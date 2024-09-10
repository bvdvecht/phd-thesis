# Instantiate the programs to run.
programs = []
er_socket_ids = {}
for i in range(N):
    dqc_program = create_dqc_client_program()
    lgt_program = create_lgt_program()
    programs.append(dqc_program)
    programs.append(lgt_program)
    er_socket_ids[dqc_program] = i  # assign unique ID for ER socket
    

# Create a thread pool that can be executed by the OS hosting the CNPU.
tpe = ThreadPoolExecutor()

# For each program, submit a piece of code that executes the whole program.
for program in programs:
    runner = program_runner(program, er_socket_ids[progam])
    tpe.submit(runner)  # submit it to the thread pool

# Block until the OS hosting the CNPU has finished all programs.
tpe.wait()


# Code for running a single program.
def program_runner(program, er_socket_id):
    # Create connection with QNPU
    qnpu_connection = connect_qnpu()

    # Use connection to setup processes.
    qnpu_connection.register_program()
    for remote_node in program.remote_nodes:
        er_socket = ERSocket(
            remote_node=remote_node.name,
            er_socket_id=er_socket_id,
            remote_er_socket_id=er_socket_id)
        qnpu_connection.open_er_socket(er_socket)
    
    # classical sockets with other programs do not go through the QNPU
    create_classical_sockets()
    

    # Execute the program code; it can use the connection to send subroutines
    # to the QNPU and receive results.
    run(program, qnpu_connection)
