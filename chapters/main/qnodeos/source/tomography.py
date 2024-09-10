# Bases to measure the final server state in.
MEAS_BASES = ["+X", "+Y", "+Z", "-X", "-Y", "-Z"]

# Local tomography code with axis and angle parameters.
class ClientLocalApp(Application):
    def __init__(self, axis: str, angle: float) -> None:
        self._axis = axis
        self._angle = angle

    def run(self, context: ApplicationContext) -> Dict[str, Any]:
        outcomes = {}
        # Loop over all 6 cardinal measurement bases.
        for basis in self.MEAS_BASES:
            # Create and initialize a qubit in the |0> state.
            q = Qubit(context.connection)
            # Rotate it to one of the 6 cardinal states.
            if self._axis == "X":
                q.rot_X(angle=self._angle)
            else:
                q.rot_Y(angle=self._angle)
            # Measure it in the current measurement basis.
            self._rotate_basis(qubit=q, basis=basis)
            outcomes[basis] = q.measure(store_array=False)
        # Compile send the subroutine containing the above instructions.
        context.connection.flush()
        return outcomes
