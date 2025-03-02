import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt

# 🔹 Thông số hệ thống
m = 0.1  # kg
g = 9.81  # m/s²
k = 10.0  # hằng số từ trường
z_eq = 0.1  # Vị trí cân bằng
I_eq = 0.5  # Dòng điện cân bằng
dt = 0.01  # Bước thời gian
N = 20  # Horizon MPC

# 🔹 Ma trận trạng thái tuyến tính hóa
A = np.array([[0, 1], [-2 * k * I_eq / (m * z_eq**3), 0]])
B = np.array([[0], [2 * k * I_eq / (m * z_eq**2)]])
C = np.array([[1, 0]])  # Chỉ lấy sai số vị trí

# 🔹 Mở rộng trạng thái với integral action
A_ext = np.block([[A, np.zeros((2, 1))], [C, np.array([[1]])]])
B_ext = np.vstack([B, np.zeros((1, 1))])

# 🔹 Ma trận chi phí mở rộng
Q_ext = np.diag([100, 1, 50])  # Thêm trọng số cho tích lũy sai số
R = np.array([[0.1]])

# 🔹 Giới hạn dòng điện
I_min, I_max = -1.0, 1.0

# 🔹 MPC Controller với Integral Action
def mpc_control(state, e, target):
    x = cp.Variable((3, N+1))  # Trạng thái mở rộng
    u = cp.Variable((1, N))  # Điều khiển

    cost = 0
    constraints = [x[:, 0] == np.hstack([state, e])]  # Điều kiện ban đầu

    for t in range(N):
        cost += cp.quad_form(x[:, t] - np.hstack([target, 0]), Q_ext) + cp.quad_form(u[:, t], R)
        constraints += [x[:, t+1] == A_ext @ x[:, t] + B_ext @ u[:, t]]
        constraints += [u[:, t] >= I_min, u[:, t] <= I_max]

    # Giải bài toán tối ưu
    prob = cp.Problem(cp.Minimize(cost), constraints)
    prob.solve()

    return u[:, 0].value, x[2, 1].value  # Trả về điều khiển và e mới

# 🔹 Mô phỏng hệ thống MagLev với MPC có Integral Action
state = np.array([0.05, 0])  # Trạng thái ban đầu [z, v]
e = 0  # Sai số tích lũy
target = np.array([z_eq, 0])  # Trạng thái mong muốn
time_steps = 200
trajectory = []

for _ in range(time_steps):
    action, e = mpc_control(state, e, target)
    state = A @ state + B @ action  # Cập nhật trạng thái
    trajectory.append(state[0])  # Lưu vị trí viên bi

# 🔹 Vẽ đồ thị quỹ đạo viên bi
time = np.arange(time_steps) * dt
plt.figure(figsize=(8, 5))
plt.plot(time, trajectory, label="Quỹ đạo viên bi (MPC với Integral Action)", linewidth=2)
plt.axhline(y=z_eq, color='r', linestyle="--", label="Vị trí mong muốn")
plt.xlabel("Thời gian (s)")
plt.ylabel("Vị trí viên bi (m)")
plt.title("MPC với Integral Action - Giảm Sai Lệch Tĩnh")
plt.legend()
plt.grid()
plt.show()
