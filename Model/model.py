from Model.cluster import Cluster
from Model.person import Person
import numpy as np
import scipy.stats
from scipy.signal import find_peaks
from cmath import *
import math
from constants import *
import matplotlib.pyplot as plt

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
d_ant = lambda_c/2  # Distance between each antenna
Ts = 1 / BW  # Sampling time   (Delta_tau) -> fast time interval  (index i)
T = (kappa + 1) * (Q + L) * Ts  # Time between the reception of two symbols  (Delta_t) -> slow time interval (index k)

"""
i in range(Q) -> fast time index, there is Q samples for the signal as theres is Q Symbols  -> i*Ts
k in range(N.M) -> slow time index, 
l in range(N_a) -> antenna index
"""

bin_i = np.arange(-Ts/2, (Q+1/2) * Ts, Ts)


def poissonPointProcess(cluster):
    lambda0 = cluster.getLambda0()
    nb_points = scipy.stats.poisson(lambda0 * cluster.getArea()).rvs()
    r = cluster.getRadius() * np.sqrt(np.random.uniform(0.0, 1.0, nb_points))
    theta = 2 * pi * np.random.uniform(0, 1, nb_points)
    x0 = [math.cos(i) for i in theta]
    y0 = [math.sin(i) for i in theta]
    x1 = np.multiply(r, x0)
    y1 = np.multiply(r, y0)
    x = [i + cluster.getX() for i in x1]
    y = [i + cluster.getY() for i in y1]

    return np.array([x, y])


class Model:
    # Constructor
    def __init__(self):
        self.map_dim        = [0, 0]
        self.clusters_list  = []
        self.points         = []
        self.tx_pos         = [0, 0]
        self.rx_pos         = [0, 0]
        self.d              = 0
        self.lambda_c       = 0

        self.M              = 64  # Number of OFDM symbols used for averaging in channel estimation
        self.N              = 64  # Number of channel estimations to obtain one RDM
        self.thresh_detection = -90
        self.pfa            = 0
        self.kcfar          = 0
        self.ncfar          = 0
        self.guard          = 0
        self.thresh_angle = -6

        self.d_res          = 0
        self.f_res          = 0
        self.v_res          = 0
        self.T_dwell        = 0
        self.alpha_res      = 0

        self.detectionMode = "Threshold"
        self.d_smaller_d_res = False
    # -- Points Function --

    def initSimulation(self, N, M, thresh_detection, pfa, kcfar, ncfar, guard, thresh_angle, detectionMode):
        self.points.clear()
        self.N = N
        self.M = M
        self.detectionMode = detectionMode
        self.pfa = pfa
        self.kcfar = kcfar
        self.guard = guard
        self.ncfar = ncfar
        self.computeResolutionParameters()
        self.thresh_detection = thresh_detection
        self.thresh_angle = thresh_angle

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

    def computeResolutionParameters(self):
        self.d_res = C / (2 * BW)
        self.f_res = 1 / (self.N * self.M * Delta_t)
        self.v_res = lambda_c / (2 * self.N * self.M * Delta_t)
        self.T_dwell = self.N * self.M * Delta_t
        self.alpha_res = 3

    def computeRDM(self):
        d_tx    = np.zeros(len(self.points), dtype=float)
        d_rx    = np.zeros(len(self.points), dtype=float)
        DoA     = np.zeros(len(self.points), dtype=float)
        f_d     = np.zeros(len(self.points), dtype=float)
        tau_n   = np.zeros(len(self.points), dtype=float)
        idx     = np.zeros(len(self.points), dtype=int)
        P_RXn   = np.zeros(len(self.points), dtype=float)

        for point in range(len(self.points)):
            d_tx[point], d_rx[point], DoA[point], f_d[point] = self.points[point].computeParameters(self.tx_pos, self.rx_pos)
            tau_n[point]    = (d_tx[point] + d_rx[point]) / C
            idx[point]      = (np.searchsorted(bin_i, tau_n[point], side='right') - 1)
            #idx[point]      = round(tau_n[point]/Ts)
            P_RXn[point]    = (P_TX * G_TX * G_RX * (lambda_c / (d_tx[point] * d_rx[point])) ** 2) / (L_RX * L_TX * (4 * pi) ** 3)

        h = np.zeros((Q, self.N * self.M, N_a), dtype=complex)  # range slow-time map

        for point in range(len(self.points)):
            i = idx[point]
            for l in range(N_a):
                for k in range(self.N * self.M):
                    h[i, k, l] = h[i, k, l] + sqrt(P_RXn[point]) \
                                 * exp(-1j * 2 * pi * f_c * tau_n[point]) \
                                 * exp(1j * 2 * pi * k * f_d[point] * T) \
                                 * exp(1j * 2 * pi * l * (d_ant / lambda_c) * sin(DoA[point]))

        n1 = np.random.normal(0, 1, (Q, self.M * self.N, N_a)) * sqrt(P_noise / 2)
        n2 = np.random.normal(0, 1, (Q, self.M * self.N, N_a)) * sqrt(P_noise / 2)
        h2 = h + n1 + n2 * 1j

        h3 = np.reshape(h2, (Q, self.M, self.N, N_a))
        h_avg = np.squeeze(np.mean(h3, axis=2))

        blackman2D = np.tile(np.blackman(self.N), (Q, 1))
        blackman3D = np.repeat(np.expand_dims(blackman2D, axis=2), repeats=N_a, axis=2)

        h_wdw = np.multiply(h_avg, blackman3D)
        RDC   = np.fft.fftshift(np.fft.fft(h_wdw, n=self.N, axis=1), axes=1)

        if self.detectionMode == "Threshold":
            RDC_reshape = RDC[0:16, int(self.N/4):3*int(self.N/4), :]
            x = np.arange(-int(self.N / 4) * self.v_res, int(self.N / 4) * self.v_res, self.v_res)
            z = 20 * np.log10(np.abs(RDC_reshape[:, :, 0]))
        else:
            RDC_reshape = RDC[0:16, :, :]
            x = np.arange(-int(self.N/2 - self.ncfar/2 - self.guard/2) * self.v_res, int(self.N/2 - self.ncfar/2 - self.guard/2) * self.v_res, self.v_res)
            z = 20 * np.log10(np.abs(RDC_reshape[:, int(self.ncfar/2+self.guard/2):int(self.N-self.ncfar/2-self.guard/2), 0]))

        y = np.arange(0, 16 * self.d_res, self.d_res)

        detection_map, idx_list = self.detectionMap(np.abs(RDC_reshape[:, :, 0]))
        h_r = np.zeros((len(idx_list), N_a), dtype=complex)
        est_nb_points = 0

        if self.detectionMode == "Threshold":
            dmap = detection_map
        else:
            dmap = detection_map[:, int(self.ncfar/2+self.guard/2):int(self.N-self.ncfar/2-self.guard/2)]

        AoA_list = []
        for i in range(len(idx_list)):
            for j in range(N_a):
                h_r[i, j] = RDC_reshape[idx_list[i][0], idx_list[i][1], j]
            AoA_list.append(10 * np.log10(np.abs(self.musicAoa(np.array(h_r[i, :])[np.newaxis]))))
            peaks, _ = find_peaks(AoA_list[i], height=self.thresh_angle)
            est_nb_points = est_nb_points + len(peaks)

        return x, y, z, dmap, AoA_list, est_nb_points

    def detectionMap(self, RDC):
        detection_map = np.zeros(RDC.shape)
        idx_list = []
        if self.detectionMode != "Threshold":
            min_j = int(self.ncfar/2+self.guard/2)
            max_j = int(self.N-self.ncfar/2-self.guard/2)
            if self.detectionMode == "OS-CFAR":
                for i in range(RDC.shape[0]):
                    for j in range(min_j, max_j):
                        x1 = RDC[i, int(j - min_j):int(j - self.guard / 2)]
                        x2 = RDC[i, int(j + self.guard / 2 + 1):int(j + min_j + 1)]
                        x = np.sort(np.concatenate((x1, x2), axis=None))
                        Pn = x[self.kcfar]
                        V_T = math.sqrt(2*Pn*math.log(1/10**self.pfa))
                        if RDC[i, j] > V_T:
                            detection_map[i, j] = 1
                            idx_list.append([i, j])
            else:
                for i in range(RDC.shape[0]):
                    for j in range(min_j, max_j):
                        sum1 = np.sum(np.square(RDC[i, int(j - min_j):int(j - self.guard / 2)]))
                        sum2 = np.sum(np.square(RDC[i, int(j + self.guard / 2 + 1):int(j + min_j + 1)]))
                        Pn = (sum1 + sum2)/self.ncfar
                        #Pn = np.sum(np.square(RDC[i, min_j:max_j]))/self.ncfar
                        V_T = math.sqrt(2*Pn*math.log(1/10**self.pfa))
                        if RDC[i, j] > V_T:
                            detection_map[i, j] = 1
                            idx_list.append([i, j])

        else:
            for i in range(RDC.shape[0]):
                if self.detectionMode == "Threshold":
                    idx, _ = find_peaks(RDC[i, :], height=10**(self.thresh_detection/20))
                    for j in range(len(idx)):
                        detection_map[i, idx[j]] = 1
                        idx_list.append([i, idx[j]])
        return detection_map, idx_list

    def musicAoa(self, h_r):
        h_r = np.transpose(h_r)

        R = np.dot(h_r, np.transpose(h_r))
        [D, V] = np.linalg.eig(R)  # eigenvalue decomposition of R. V = eigenvectors, D = eigenvalues
        I = np.argsort(-np.abs(D))
        D = -np.sort(-np.abs(D))

        V = V[:, I]
        Us = V[:, 0]
        Un = V[:, 1:]
        G = np.dot(Un, np.transpose(Un))
        angles = np.arange(-90, 90.05, 0.05)
        # Check multiplication of vector
        s = np.sin(angles * pi / 180)
        v = np.exp(1j * 2 * pi * f_c / 3e8 * d_ant * np.dot(np.arange(N_a).reshape(N_a, 1), s.reshape(1, s.size)))

        music_spectrum = np.zeros(angles.size, dtype=complex)
        for k in range(angles.size):
            music_spectrum[k] = 1 / np.dot(np.dot(v[:, k], G), v[:, k])

        music_spectrum = music_spectrum / np.max(abs(music_spectrum))
        return music_spectrum

    # -- Cluster Functions --
    def addCluster(self, r, x, y, v, theta, lambda0, color, is_point):
        self.clusters_list.append(Cluster(r, x, y, v, theta, lambda0, color, is_point))

    def removeCluster(self, index):
        del self.clusters_list[index]

    def updateClusterSettings(self, r, x, y, v, theta, lambda0, index):
        self.clusters_list[index].updateClusterSettings(r, x, y, v, theta, lambda0)

    def setIsPoint(self, is_point, index):
        self.clusters_list[index].setIsPoint(is_point)

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