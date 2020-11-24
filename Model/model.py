from Model.cluster import Cluster
from Model.person import Person
import numpy as np
import scipy.stats
from cmath import *
from constants import *

P_TX = 1  # Power of the transmitter
G_TX = 1  # Gain of the transmitter
G_RX = 1  # Gain of the receiver
L_TX = 1  # Losses at the transmitting side
L_RX = 1  # Losses at the receiving sid
N0_dBm = -174  #PSD of noise [dBm/Hz]
N0 = 10**(N0_dBm/10-3)  #PSD of noise [W/Hz]

f_c = 5e9  # Carrier frequency
BW = 80e6  # Bandwidth
Q = 1024  # Number of OFDM carriers
L = 64  # Number of taps in the channel, corresponding to a duration of L*Delta_tau
M = 64  # Number of OFDM symbols used for averaging in channel estimation
N = 64  # Number of channel estimations to obtain one RDM
N_a = 4  # Number of antennas at the receiver
d_ant = 0.06  # Distance between each antenna
kappa = 0  # Number of unknown data OFDM

lambda_c = C / f_c  # Wavelength
Ts = 1 / BW  # Sampling time   (Delta_tau) -> fast time interval  (index i)
T = (kappa + 1) * (Q + L) * Ts  # Time between the reception of two symbols  (Delta_t) -> slow time interval (index k)

"""
i in range(Q) -> fast time index, there is Q samples for the signal as theres is Q Symbols  -> i*Ts
k in range(N.M) -> slow time index, 
l in range(N_a) -> antenna index
"""

Delta_t = 16e-6
# Resolution
d_res = C / (2 * BW)
f_res = 1 / (N * M * Delta_t)
v_res = lambda_c / (2 * N * M * Delta_t)
T_dwell = N * M * Delta_t
alpha_res = 3
P_noise = N0*BW
bin_i = np.arange(0, Q*Ts, Ts)


def poissonPointProcess(cluster):
    lambda0 = cluster.getLambda0()
    nb_points = scipy.stats.poisson(lambda0 * cluster.getArea()).rvs()
    r = cluster.getRadius() * np.random.uniform(0, 1, nb_points)
    theta = 2 * pi * np.random.uniform(0, 1, nb_points)
    x0 = [cos(i) for i in theta]
    y0 = [sin(i) for i in theta]
    x1 = np.multiply(r, x0)
    y1 = np.multiply(r, y0)
    x = [i + cluster.getX() for i in x1]
    y = [i + cluster.getY() for i in y1]

    return np.array([x, y])


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

    # -- Points Function --

    def initSimulation(self):
        self.points.clear()

        for cluster in self.clusters_list:
            temp_pos_list = poissonPointProcess(cluster)
            v = cluster.getSpeed()
            theta = cluster.getAngle()
            color = cluster.getColor()
            for i in range(0, temp_pos_list.shape[1]):
                self.points.append(Person(temp_pos_list[0, i], temp_pos_list[1, i], v, theta, lambda_c, color))

        self.d = sqrt((self.tx_pos[0] - self.rx_pos[0]) ** 2 + (self.tx_pos[1] - self.rx_pos[1]) ** 2)

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

    def computeParameters(self):
        d_tx = np.zeros(len(self.points), dtype=float)
        d_rx = np.zeros(len(self.points), dtype=float)
        DoA = np.zeros(len(self.points), dtype=float)
        f_d = np.zeros(len(self.points), dtype=float)
        tau_n = np.zeros(len(self.points), dtype=float)
        idx = np.zeros(len(self.points), dtype=int)
        P_RXn = np.zeros(len(self.points), dtype=float)

        for point in range(len(self.points)):
            d_tx[point], d_rx[point], DoA[point], f_d[point] = self.points[point].computeParameters(self.tx_pos, self.rx_pos)
            tau_n[point] = (d_tx[point] + d_rx[point]) / C
            idx[point] = (np.searchsorted(bin_i, tau_n[point], side='right') - 1)
            P_RXn[point] = (P_TX * G_TX * G_RX * (lambda_c / (d_tx[point] * d_rx[point])) ** 2) / (L_RX * L_TX * (4 * pi) ** 3)

        h = np.zeros((Q, N*M, N_a), dtype=complex)   # range slow-time map
        h2 = np.zeros((Q, M, N, N_a), dtype=complex)
        h_avg = np.zeros((Q, N, N_a), dtype=complex)
        H = np.zeros((Q, N, N_a), dtype=float)
        W = np.zeros((Q, N, N_a), dtype=float)

        for point in range(len(self.points)):
            i = idx[point]
            for l in range(N_a):
                for k in range(N*M):
                    h[i, k, l] = h[i, k, l] + sqrt(P_RXn[point]) * exp(-1j * 2 * pi * f_c * tau_n[point]) * exp(1j * 2 * pi * k * f_d[point] * T) * exp(
                           1j * 2 * pi * l * (d_ant / lambda_c) * sin(DoA[point]))

        h2 = np.reshape(h, (Q, M, N, N_a))
        h_avg = np.squeeze(np.mean(h2, 2))

        H = np.fft.fftshift(np.fft.fft(h_avg, n=N, axis=1), axes=1)

        W = np.random.normal(0, 1, (Q, N, N_a))*sqrt(P_noise)

        H2 = H + W

        x = np.arange(-N/4*v_res, N/4*v_res, v_res)
        y = np.arange(0, 30*d_res, d_res)
        z = 20*np.log10(np.abs(H2[0:30, int(N/4):int(3*N/4), 1]))
        """
        fig = plt.figure()
        # ax = fig.gca(projection='3d')
        z = np.abs(H[0:10, :, 1])
        # X, Y = np.meshgrid(x, np.arange(0, 50*d_res, d_res))
        # surf = ax.plot_surface(X, Y, absH, cmap=cm.coolwarm,
        #                linewidth=0, antialiased=False)
        #z_min, z_max = -z.max(), z.min()
        pc = plt.pcolormesh(x, y, z, cmap='jet', shading='auto')#, vmin=z_min, vmax=z_max)
        fig.colorbar(pc)
        plt.show()
        """

        return x, y, z

    # -- Cluster Functions --

    def addCluster(self, r, x, y, v, theta, lambda0, color):
        self.clusters_list.append(Cluster(r, x, y, v, theta, lambda0, color))

    def removeCluster(self, index):
        del self.clusters_list[index]

    def updateClusterSettings(self, r, x, y, v, theta, lambda0, index):
        self.clusters_list[index].updateClusterSettings(r, x, y, v, theta, lambda0)

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
