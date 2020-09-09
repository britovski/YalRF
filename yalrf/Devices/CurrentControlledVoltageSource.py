class CurrentControlledVoltageSource():
    
    def __init__(self, name, n1, n2, n3, n4, G=1, tau=0):
        self.name = name
        self.n1   = n1
        self.n2   = n2
        self.n3   = n3
        self.n4   = n4
        self.G    = float(G)
        self.tau  = float(tau)

    def get_num_vsources(self, analysis):
        return 2

    def is_nonlinear(self):
        return False

    def init(self):
        pass

    def add_dc_stamps(self, A, z, x, iidx):
        A[iidx][self.n2] = +1.0
        A[iidx][self.n3] = -1.0 
        A[iidx][iidx] = -self.G
        A[iidx+1][self.n1] = +1.0
        A[iidx+1][self.n4] = -1.0
        A[self.n1][iidx] = +1.0
        A[self.n4][iidx] = -1.0
        A[self.n2][iidx+1] = +1.0
        A[self.n3][iidx+1] = -1.0

    def add_ac_stamps(self, A, z, x, iidx, freq):
        G = self.G * np.exp(-1j * 2. * np.pi * freq * self.tau)
        A[iidx][self.n2] = +1.0
        A[iidx][self.n3] = -1.0 
        A[iidx][iidx] = -G
        A[iidx+1][self.n1] = +1.0
        A[iidx+1][self.n4] = -1.0
        A[self.n1][iidx] = +1.0
        A[self.n4][iidx] = -1.0
        A[self.n2][iidx+1] = +1.0
        A[self.n3][iidx+1] = -1.0

    # TODO: implement transient time delay
    def add_tran_stamps(self, A, z, x, iidx, xt, t, tstep):
        self.add_dc_stamps(A, z, x, iidx)

    def __str__(self):
        return 'CCVS: {}\nNodes = {} -> {} and {}->{}\nG = {}\ndelay={}\n'.format(self.name, self.n1, self.n2, self.n3, self.n4, self.G, self.tau)

