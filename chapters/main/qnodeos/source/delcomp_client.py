# Bases to measure the final server state in.
# Note: for efficiency reasons, only bases +Y and -Y were
# used for alpha=pi/2, and +Z and -Z for alpha=pi.
MEAS_BASES = ["+X", "+Y", "+Z", "-X", "-Y", "-Z"]

# Client code, with parameters alpha and theta.
class DelegatedComputationClient(Application):
    def __init__(self, alpha: float, theta: float):
        self._theta = theta
        self._alpha = alpha

    def run(self, context: ApplicationContext) -> Dict[str, Any]:
        outcomes = {}
        for basis in MEAS_BASES:
            # Create EPR pair with server
            epr = context.epr_sockets[0].create_keep()[0]
            # Local gates
            epr.rot_Y(angle=math.pi / 2)
            epr.rot_X(angle=self._theta)
            epr.rot_X(angle=math.pi)
            # Measurement
            m_c = epr.measure(store_array=False)
            # Compile and send subroutine C1
            context.connection.flush()
            # Receive and store result (m_c).
            outcomes[basis] = m_c
            # Compute and send delta.
            delta = self._alpha - self._theta + m_c * math.pi
            context.app_socket.send_float(delta)
        return outcomes