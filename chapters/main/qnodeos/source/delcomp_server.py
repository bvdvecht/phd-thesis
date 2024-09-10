# Bases to measure the final server state in.
# Note: for efficiency reasons, only bases +Y and -Y were
# used for alpha=pi/2, and +Z and -Z for alpha=pi.
MEAS_BASES = ["+X", "+Y", "+Z", "-X", "-Y", "-Z"]

# Server code (no parameters).
class DelegatedComputationServer(Application):
    def _rotate_basis(self, qubit: Qubit, basis: str) -> None:
        right_angle = math.pi / 2
        if basis == "+X":
            qubit.rot_Y(angle=-right_angle)
        elif basis == "+Y":
            qubit.rot_X(angle=right_angle)
        elif basis == "-X":
            qubit.rot_Y(angle=right_angle)
        elif basis == "-Y":
            qubit.rot_X(angle=-right_angle)
        elif basis == "-Z":
            qubit.X()

    def run(self, context: ApplicationContext) -> Dict[str, Any]:
        outcomes = {}
        for basis in MEAS_BASES:
            # Create EPR pair with client
            epr = context.epr_sockets[0].recv_keep()[0]
            # Compile and send subroutine S1.
            context.connection.flush()
            # Wait and receive delta from client.
            delta = context.app_socket.recv_float()
            # Local gates using delta.
            epr.rot_Y(angle=math.pi / 2)
            epr.rot_X(angle=delta)
            epr.rot_X(angle=math.pi)
            # At this point, the server has qubit state |psi>.
            # Measure in particular basis (part of tomography).
            self._rotate_basis(qubit=epr, basis=basis)
            m_s = epr.measure(store_array=False)
            # Compile and send subroutine S2.
            context.connection.flush()
            # Receive and store result (m_s).
            m_s = int(m_s)
            outcomes[basis] = m_s
        return outcomes
