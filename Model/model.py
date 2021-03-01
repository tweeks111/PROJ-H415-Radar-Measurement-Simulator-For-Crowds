from Model.cluster import Cluster
from Model.person import Person
import numpy as np
import scipy.stats
from scipy.signal import find_peaks
from cmath import *
import math
from constants import *
import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


f_c = 5e9  # Carrier frequency
BW = 80e6  # Bandwidth
Q = 1024  # Number of OFDM carriers
L = 64  # Number of taps in the channel, corresponding to a duration of L*Delta_tau
N_a = 4  # Number of antennas at the receiver
kappa = 0  # Number of unknown data OFDM
Delta_t = 16e-6

P_TX = 1  # Power of the transmitter
G_TX = 1  # Gain of the transmitter
G_RX = 1  # Gain of the receiver
L_TX = 1  # Losses at the transmitting side
L_RX = 1  # Losses at the receiving sid
N0_dBm = -174  # PSD of noise [dBm/Hz]
N0 = 10 ** (N0_dBm / 10 - 3)  # PSD of noise [W/Hz]
P_noise = N0 * BW

lambda_c = C / f_c  # Wavelength
d_ant = lambda_c / 2  # Distance between each antenna
Ts = 1 / BW  # Sampling time   (Delta_tau) -> fast time interval  (index i)
T = (kappa + 1) * (Q + L) * Ts  # Time between the reception of two symbols  (Delta_t) -> slow time interval (index k)

"""
i in range(Q) -> fast time index, there is Q samples for the signal as theres is Q Symbols  -> i*Ts
k in range(N.M) -> slow time index, 
l in range(N_a) -> antenna index
"""

bin_i = np.arange(-Ts / 2, (Q + 1 / 2) * Ts, Ts)


class Model:
    # Constructor
    def __init__(self):
        self.map_dim = [0, 0]
        self.clusters_list = []
        self.points = []
        self.tx_pos = [0, 0]
        self.rx_pos = [0, 0]
        self.d = 0
        self.lambda_c = 0

        self.M = 64  # Number of OFDM symbols used for averaging in channel estimation
        self.N = 64  # Number of channel estimations to obtain one RDM

        self.d_res = 0
        self.f_res = 0
        self.v_res = 0
        self.T_dwell = 0
        self.alpha_res = 0

        self.d_smaller_d_res = False

    # -- Points Function --

    def initSimulation(self, N, M):
        self.computeResolutionParameters(N, M)
        self.initClusters()

    def initAnalysis(self, N, M):
        self.computeResolutionParameters(N, M)
        self.initClusters()

    def updatePointsPosition(self, time):
        pos_list = []
        for point in self.points:
            [new_x, new_y] = point.computeNewPos(time)
            if new_x < 0 or new_x > self.map_dim[0]:
                point.oppositeVX()
            if new_y < 0 or new_y > self.map_dim[1]:
                point.oppositeVY()
            point.updatePos(time)
            pos_list.append(point.getPos())

        return pos_list

    # -- RDM Computation --

    def computeResolutionParameters(self, N, M):
        self.d_res = C / (2 * BW)
        self.f_res = 1 / (N * M * Delta_t)
        self.v_res = lambda_c / (2 * N * M * Delta_t)
        self.T_dwell = N * M * Delta_t
        self.alpha_res = 3

    def runAnalysis(self, RDAC, detection_list):
        N, M = detection_list[0], detection_list[1]
        ncfar = 0
        guard = 0
        detection_mode = detection_list[2]
        thresh_angle = detection_list[-1]

        if detection_mode == "Peak Detection":
            RDAC_reshape = RDAC[0:16, int(N / 4):3 * int(N / 4), :]
        else:
            ncfar = detection_list[4]
            guard = detection_list[5]
            RDAC_reshape = RDAC[0:16, :, :]
        detection_map, idx_list = detectionMap(np.abs(RDAC_reshape[:, :, 0]), detection_list, N)
        AoA_list, est_nb_points = computeAllAoA(RDAC_reshape, idx_list, thresh_angle)

        return est_nb_points

    def runSimulation(self, detection_list):
        N, M = detection_list[0], detection_list[1]
        RDAC = self.computeRDM(N, M)
        ncfar = 0
        guard = 0
        detection_mode = detection_list[2]
        thresh_angle = detection_list[-1]
        if detection_mode == "Peak Detection":
            RDAC_reshape = RDAC[0:16, int(N / 4):3 * int(N / 4), :]
            x = np.arange(-int(N / 4) * self.v_res, int(N / 4) * self.v_res, self.v_res)
            z = 20 * np.log10(np.abs(RDAC_reshape[:, :, 0]))
        else:
            ncfar = detection_list[4]
            guard = detection_list[5]
            RDAC_reshape = RDAC[0:16, :, :]
            x = np.arange(-int(N / 2 - ncfar / 2 - guard / 2) * self.v_res,
                          int(N / 2 - ncfar / 2 - guard / 2) * self.v_res, self.v_res)
            z = 20 * np.log10(np.abs(
                RDAC_reshape[:, int(ncfar / 2 + guard / 2):int(N - ncfar / 2 - guard / 2), 0]))
        y = np.arange(0, 16 * self.d_res, self.d_res)

        detection_map, idx_list = detectionMap(np.abs(RDAC_reshape[:, :, 0]), detection_list, N)

        AoA_list, est_nb_points = computeAllAoA(RDAC_reshape, idx_list, thresh_angle)

        if detection_mode == "Peak Detection":
            dmap = detection_map
        else:
            dmap = detection_map[:, int(ncfar / 2 + guard / 2):int(N - ncfar / 2 - guard / 2)]

        return x, y, z, dmap, AoA_list, est_nb_points

    def computeRDM(self, N, M):
        d_tx = np.zeros(len(self.points), dtype=float)
        d_rx = np.zeros(len(self.points), dtype=float)
        DoA = np.zeros(len(self.points), dtype=float)
        f_d = np.zeros(len(self.points), dtype=float)
        tau_n = np.zeros(len(self.points), dtype=float)
        idx = np.zeros(len(self.points), dtype=int)
        P_RXn = np.zeros(len(self.points), dtype=float)

        for point in range(len(self.points)):
            d_tx[point], d_rx[point], DoA[point], f_d[point] = self.points[point].computeParameters(self.tx_pos,
                                                                                                    self.rx_pos)
            tau_n[point] = (d_tx[point] + d_rx[point]) / C
            idx[point] = (np.searchsorted(bin_i, tau_n[point], side='right') - 1)
            # idx[point]      = round(tau_n[point]/Ts)
            P_RXn[point] = (P_TX * G_TX * G_RX * (lambda_c / (d_tx[point] * d_rx[point])) ** 2) / (
                    L_RX * L_TX * (4 * pi) ** 3)

        h = np.zeros((Q, N * M, N_a), dtype=complex)  # range slow-time map

        for point in range(len(self.points)):
            i = idx[point]
            for l in range(N_a):
                for k in range(N * M):
                    h[i, k, l] = h[i, k, l] + sqrt(P_RXn[point]) \
                                 * exp(-1j * 2 * pi * f_c * tau_n[point]) \
                                 * exp(1j * 2 * pi * k * f_d[point] * T) \
                                 * exp(1j * 2 * pi * l * (d_ant / lambda_c) * sin(DoA[point]))

        for point in range(len(self.points)):
            i = idx[point]


        n1 = np.random.normal(0, 1, (Q, M * N, N_a)) * sqrt(P_noise / 2)
        n2 = np.random.normal(0, 1, (Q, M * N, N_a)) * sqrt(P_noise / 2)
        h2 = h + n1 + n2 * 1j

        h3 = np.reshape(h2, (Q, N, M, N_a))
        h_avg = np.squeeze(np.mean(h3, axis=2))
        blackman2D = np.tile(np.blackman(N), (Q, 1))
        blackman3D = np.repeat(np.expand_dims(blackman2D, axis=2), repeats=N_a, axis=2)
        h_wdw = np.multiply(h_avg, blackman3D)
        RDAC = np.fft.fftshift(np.fft.fft(h_wdw, n=N, axis=1), axes=1)

        return RDAC

    # -- Cluster Functions --
    def addCluster(self, r, x, y, v, theta, lambda0, color, is_point):
        self.clusters_list.append(Cluster(r, x, y, v, theta, lambda0, color, is_point))

    def removeCluster(self, index):
        del self.clusters_list[index]

    def updateClusterSettings(self, r, x, y, v, theta, lambda0, index):
        self.clusters_list[index].updateClusterSettings(r, x, y, v, theta, lambda0)

    def setIsPoint(self, is_point, index):
        self.clusters_list[index].setIsPoint(is_point)

    def initClusters(self):
        self.points.clear()
        for cluster in self.clusters_list:
            if cluster.is_point == 0:
                temp_pos_list = poissonPointProcess(cluster)
            else:
                temp_pos_list = np.array([[cluster.getX()], [cluster.getY()]])
            v = cluster.getSpeed()
            theta = cluster.getAngle()
            color = cluster.getColor()
            for i in range(0, temp_pos_list.shape[1]):
                self.points.append(Person(temp_pos_list[0, i], temp_pos_list[1, i], v, theta, lambda_c, color))

    # -- Set Functions --

    def setMapDim(self, map_dim):
        self.map_dim = map_dim

    def setRadarPos(self, tx_pos, rx_pos):
        self.tx_pos = tx_pos
        self.rx_pos = rx_pos

    # -- Get Functions --

    def getClusterSettings(self, index):
        return self.clusters_list[index].getClusterSettings()

    def getPointsPosition(self):
        pos_list = []
        for point in self.points:
            pos_list.append([point.getX(), point.getY()])
        return pos_list

    def getPointsColor(self):
        color_list = []
        for point in self.points:
            color_list.append(point.getColor())
        return color_list

    def getRadarPosition(self):
        return self.tx_pos, self.rx_pos

    def getRadarIsSmaller(self):
        self.d = math.sqrt((self.tx_pos[0] - self.rx_pos[0]) ** 2 + (self.tx_pos[1] - self.rx_pos[1]) ** 2)
        if self.d < self.d_res:
            self.d_smaller_d_res = True
        else:
            self.d_smaller_d_res = False
        return self.d_smaller_d_res

    def getNbPoints(self):
        return len(self.points)


def musicAoa(h_r):
    h_r = np.transpose(h_r)
    R = np.dot(h_r, np.transpose(h_r.conj()))
    [D, V] = np.linalg.eig(R)  # eigenvalue decomposition of R. V = eigenvectors, D = eigenvalues
    I = np.argsort(-np.abs(D))
    D = -np.sort(-np.abs(D))

    V = V[:, I]
    Us = V[:, 0]
    Un = V[:, 1:]
    G = np.dot(Un, np.transpose(Un.conj()))
    angles = np.arange(-90, 90.05, 0.05)
    # Check multiplication of vector
    s = np.sin(angles * pi / 180)
    v = np.exp(1j * 2 * pi * f_c / 3e8 * d_ant * np.dot(np.arange(N_a).reshape(N_a, 1), s.reshape(1, s.size)))

    music_spectrum = np.zeros(angles.size, dtype=complex)
    for k in range(angles.size):
        music_spectrum[k] = 1 / np.dot(np.dot(v[:, k].conj(), G), v[:, k])

    music_spectrum = music_spectrum / np.max(abs(music_spectrum))
    return music_spectrum

def poissonPointProcess(cluster):
    lambda0 = cluster.getLambda0()
    nb_points = 0
    while nb_points == 0:
        nb_points = scipy.stats.poisson(lambda0 * cluster.getArea()).rvs()
    r = cluster.getRadius() * np.random.uniform(0.0, 1.0, nb_points)
    theta = 2 * pi * np.random.uniform(0, 1, nb_points)
    x0 = [math.cos(i) for i in theta]
    y0 = [math.sin(i) for i in theta]
    x1 = np.multiply(r, x0)
    y1 = np.multiply(r, y0)
    x = [i + cluster.getX() for i in x1]
    y = [i + cluster.getY() for i in y1]

    return np.array([x, y])


def detectionMap(RDAC, detection_list, N):
    detection_map = np.zeros(RDAC.shape)
    idx_list = []
    detection_mode = detection_list[2]
    if detection_mode != "Peak Detection":
        pfa = detection_list[3]
        ncfar = detection_list[4]
        guard = detection_list[5]
        min_j = int(ncfar / 2 + guard / 2)
        max_j = int(N - ncfar / 2 - guard / 2)
        if detection_mode == "OS-CFAR":
            kcfar = detection_list[6]
            for i in range(RDAC.shape[0]):
                for j in range(min_j, max_j):
                    x1 = RDAC[i, int(j - min_j):int(j - guard / 2)]
                    x2 = RDAC[i, int(j + guard / 2 + 1):int(j + min_j + 1)]
                    x = np.sort(np.concatenate((x1, x2), axis=None))
                    Pn = x[kcfar]**2
                    V_T = math.sqrt(2 * Pn * math.log(1 / 10 ** pfa))
                    if RDAC[i, j] > V_T:
                        detection_map[i, j] = 1
                        idx_list.append([i, j])
        else:
            for i in range(RDAC.shape[0]):
                for j in range(min_j, max_j):
                    sum1 = np.sum(np.square(RDAC[i, int(j - min_j):int(j - guard / 2)]))
                    sum2 = np.sum(np.square(RDAC[i, int(j + guard / 2 + 1):int(j + min_j + 1)]))
                    Pn = (sum1 + sum2) / ncfar
                    alpha = N*((10 ** pfa)**(-1/ncfar)-1)
                    T = alpha * Pn
                    #V_T = math.sqrt(2 * Pn * math.log(1 / 10 ** pfa))
                    if RDAC[i, j] > sqrt(T):
                        detection_map[i, j] = 1
                        idx_list.append([i, j])

    else:
        thresh_detection = detection_list[3]
        for i in range(RDAC.shape[0]):
            idx, _ = find_peaks(RDAC[i, :], height=10 ** (thresh_detection / 20))
            for j in range(len(idx)):
                detection_map[i, idx[j]] = 1
                idx_list.append([i, idx[j]])

    return detection_map, idx_list


def computeAllAoA(RDAC, idx_list, thresh_angle):
    AoA_list = []
    est_nb_points = 0
    h_r = np.zeros((len(idx_list), N_a), dtype=complex)
    for i in range(len(idx_list)):
        for j in range(N_a):
            h_r[i, j] = RDAC[idx_list[i][0], idx_list[i][1], j]
        AoA_list.append(10 * np.log10(np.abs(musicAoa(np.array(h_r[i, :])[np.newaxis]))))
        peaks, _ = find_peaks(AoA_list[i], height=thresh_angle)
        est_nb_points = est_nb_points + len(peaks)
    return AoA_list, est_nb_points



