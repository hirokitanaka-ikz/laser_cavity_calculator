import numpy as np

class CavityCalculator:
    
    def __init__(self):
        # all units in mm
        self.wavelength = None # wavelength in mm
        self.list_elements = list()
        self.list_spaces = list()
        self.cavity_length = None
        self.dz = 0.01 # to be modified!
        self.matrix_rt_x = np.matrix([ [1, 0], [0, 1] ]) # roundtrip matrix x
        self.matrix_rt_y = np.matrix([ [1, 0], [0, 1] ]) # roundtrip matrix y
        self.q0x = None
        self.q0y = None
        self.__initialize_results()
    

    def initialize_elements(self):
        self.list_elements = list()
        self.list_spaces = list()
    

    def __initialize_results(self):
        self.stability_x = 0.0
        self.stability_y = 0.0
        self.z = np.array([])
        self.qx = np.array([])
        self.qy = np.array([])
        self.beam_radius_x = np.array([])
        self.beam_radius_y = np.array([])
    

    def get_cavity_mode(self):
        return self.z, self.beam_radius_x, self.beam_radius_y
    

    def get_stability(self):
        self.stability_x = np.absolute(self.matrix_rt_x[0, 0] + self.matrix_rt_x[1, 1])
        self.stability_y = np.absolute(self.matrix_rt_y[0, 0] + self.matrix_rt_y[1, 1])
        return self.stability_x, self.stability_y
    

    def set_wavelength(self, wavelength_nm):
        wavelength_mm = wavelength_nm * 1e-6
        self.wavelength = wavelength_mm
    

    def __set_cavity_length(self):
        cavity_length = self.list_elements[-1]['position']
        self.cavity_length = cavity_length
    
    
    def show_elements(self):
        print('-----Cavity Elements-----')
        for i, element in enumerate(self.list_elements):
            if element['type'] == 'mirror':
                self.__show_mirror(i, element)
            elif element['type'] == 'lens':
                self.__show_mirror(i, element)
            elif element['type'] in ('front_interface', 'rear_interface'):
                self.__show_interface(i, element)
        print('-------------------------')
            

    def __show_mirror(self, number, element):
        name = element['name']
        position = element['position']
        RoC = element['RoC']
        AoI = element['AoI']
        print(f'{number}: {name}, z={position}, RoC={RoC}, AoI={AoI}deg')
    

    def __show_lens(self, number, element):
        name = element['name']
        position = element['position']
        focal_length = element['focal_length']
        print(f'{number}: {name}, z={position}, f={focal_length}')
    

    def __show_interface(self, number, element):
        name = element['name']
        position = element['position']
        n = element['refractive_index']
        AoI = element['AoI']
        print(f'{number}: {name}, z={position}, n={n}, AoI={AoI}deg')


    def __sort_elements(self):
        self.list_elements.sort(key=lambda x: x['position'])
    

    def add_mirror(self, name:str, position:float, RoC:float, AoI_deg:float):
        AoI_rad = AoI_deg / 180 * np.pi
        fx = 0.5 * RoC * np.cos(AoI_rad)
        fy = 0.5 * RoC / np.cos(AoI_rad)
        mirror = {
            'type': 'mirror',
            'name': name,
            'position': position,
            'RoC': RoC,
            'AoI': AoI_deg,
            'matrix_x': np.matrix( [ [1, 0], [1/fx, 1] ] ),
            'matrix_y': np.matrix( [ [1, 0], [1/fy, 1] ] )
        }
        self.list_elements.append(mirror)
    

    def add_front_interface(self, name:str, position:float, refractive_index:float, AoI_deg:float):
        n1 = 1.0
        n2 = refractive_index
        theta1 = AoI_deg / 180 * np.pi
        theta2 = self.__Snells_law(n1, n2, theta1)
        interface1 = {
            'type': 'front_interface',
            'name': name,
            'position': position,
            'refractive_index': refractive_index,
            'AoI': AoI_deg,
            'matrix_x1': np.matrix( [[np.cos(theta2)/np.cos(theta1), 0], [0, n1*np.cos(theta1)/n2/np.cos(theta2)]] ),
            'matrix_y1': np.matrix( [ [1, 0], [0, n1/n2] ] ),
            'matrix_x2': np.matrix( [[np.cos(theta1)/np.cos(theta2), 0], [0, n2*np.cos(theta2)/n1/np.cos(theta1)]] ),
            'matrix_y2': np.matrix( [[1, 0], [0, n2/n1]] )
        }
        self.list_elements.append(interface1)
    

    def add_rear_interface(self, name:str, position:float, refractive_index:float, AoI_deg:float):
        n1 = refractive_index
        n2 = 1.0
        theta2 = AoI_deg / 180 * np.pi
        theta1 = self.__Snells_law(n2, n1, theta2)
        interface2 = {
            'type': 'rear_interface',
            'name': name,
            'position': position,
            'refractive_index': refractive_index,
            'AoI': AoI_deg, # AoI from outside to inside
            'matrix_x1': np.matrix( [[np.cos(theta2)/np.cos(theta1), 0], [0, n1*np.cos(theta1)/n2/np.cos(theta2)]] ),
            'matrix_y1': np.matrix( [ [1, 0], [0, n1/n2] ] ),
            'matrix_x2': np.matrix( [[np.cos(theta1)/np.cos(theta2), 0], [0, n2*np.cos(theta2)/n1/np.cos(theta1)]] ),
            'matrix_y2': np.matrix( [[1, 0], [0, n2/n1]] )
        }
        self.list_elements.append(interface2)
    

    def add_lens(self, name:str, position:float, focal_length:float):
        lens = {
            'type': 'lens',
            'name': name,
            'position': position,
            'focal_length': focal_length,
            'matrix': np.matrix( [ [1, 0], [-1/focal_length, 1] ] )
        }
        self.list_elements.append(lens)
    

    def __Snells_law(self, n1, n2, theta1_rad):
        theta2 = np.arcsin(n1/n2 * np.sin(theta1_rad))
        return theta2
    

    def set_spaces(self):
        self.__sort_elements()
        for i in range(len(self.list_elements) - 1):
            position1 = self.list_elements[i]['position']
            position2 = self.list_elements[i+1]['position']
            distance = position2 - position1
            if self.list_elements[i]['type'] == 'front_interface':
                refractive_index = self.list_elements[i]['refractive_index']
            else:
                refractive_index = 1.0
            space = {
                'type': 'space',
                'range': [position1, position2],
                'refractive_index': refractive_index,
                'matrix': np.matrix( [ [1, distance], [0, 1] ] )
            }
            self.list_spaces.append(space)
    

    def set_roundtrip_matrix(self):
        self.matrix_rt_x = np.matrix([ [1, 0], [0, 1] ]) # roundtrip matrix x
        self.matrix_rt_y = np.matrix([ [1, 0], [0, 1] ]) # roundtrip matrix y
        # end mirror 1 is applied as the last element
        # forward propagation
        for element, space in zip(self.list_elements[1:], self.list_spaces):
            self.matrix_rt_x = space['matrix'] * self.matrix_rt_x
            self.matrix_rt_y = space['matrix'] * self.matrix_rt_y
            if element['type'] == 'mirror':
                self.matrix_rt_x = element['matrix_x'] * self.matrix_rt_x
                self.matrix_rt_y = element['matrix_y'] * self.matrix_rt_y
            elif element['type'] == 'front_interface':
                self.matrix_rt_x = element['matrix_x1'] * self.matrix_rt_x
                self.matrix_rt_y = element['matrix_y1'] * self.matrix_rt_y

        # backward propagation
        for element, space in zip(self.list_elements[:-1][::-1], self.list_spaces[::-1]):
            self.matrix_rt_x = space['matrix'] * self.matrix_rt_x
            self.matrix_rt_y = space['matrix'] * self.matrix_rt_y
            if element['type'] == 'mirror':
                self.matrix_rt_x = element['matrix_x'] * self.matrix_rt_x
                self.matrix_rt_y = element['matrix_y'] * self.matrix_rt_y
            elif element['type'] == 'rear_interface':
                self.matrix_rt_x = element['matrix_x2'] * self.matrix_rt_x
                self.matrix_rt_y = element['matrix_y2'] * self.matrix_rt_y
        # print(self.matrix_rt_x)
        # print(self.matrix_rt_y)
    

    def check_cavity_stability(self):
        self.stability_x = np.absolute(self.matrix_rt_x[0, 0] + self.matrix_rt_x[1, 1])
        # print(f'Stability X: {stability_x:.5f}')
        self.stability_y = np.absolute(self.matrix_rt_y[0, 0] + self.matrix_rt_y[1, 1])
        # print(f'Stability Y: {stability_y:.5f}')
        return (self.stability_x < 2, self.stability_y < 2)
    

    def __apply_element(self, qin_x, qin_y, element):
        if element['type'] in ('mirror', 'lens'):
            matrix_x = element['matrix_x']
            matrix_y = element['matrix_y']
        elif element['type'] in ('front_interface', 'rear_interface'):
            matrix_x = element['matrix_x1']
            matrix_y = element['matrix_y1']
        qout_x = (matrix_x[0, 0] * qin_x + matrix_x[0, 1]) / (matrix_x[1, 0] * qin_x + matrix_x[1, 1])
        qout_y = (matrix_y[0, 0] * qin_y + matrix_y[0, 1]) / (matrix_y[1, 0] * qin_y + matrix_y[1, 1])
        return qout_x, qout_y
    

    def __set_q0(self):
        # calculate q-parameter on the end mirror 1
        Ax = self.matrix_rt_x[0, 0]
        Bx = self.matrix_rt_x[0, 1]
        # Cx = self.matrix_rt_x[1, 0]
        Dx = self.matrix_rt_x[1, 1]

        Ay = self.matrix_rt_y[0, 0]
        By = self.matrix_rt_y[0, 1]
        # Cy = self.matrix_rt_y[1, 0]
        Dy = self.matrix_rt_y[1, 1]

        self.q0x = ( (Dx - Ax)*0.5/Bx - 1j*0.5/Bx*(4 - (Ax+Dx)**2)**0.5 )**(-1)
        self.q0y = ( (Dy - Ay)*0.5/By - 1j*0.5/By*(4 - (Ay+Dy)**2)**0.5 )**(-1)
        # print(self.q0x)
        # print(self.q0y)

    def set_cavity_mode(self):
        self.__initialize_results()
        self.__set_cavity_length()
        self.__set_q0()

        q0x = self.q0x
        q0y = self.q0y
        for space, element in zip(self.list_spaces, self.list_elements[1:]):
            z = np.arange(0, space['range'][1] - space['range'][0], self.dz)
            n = space['refractive_index']

            qx = q0x + z
            qy = q0y + z
            q0x, q0y = self.__apply_element(qx[-1], qy[-1], element)

            self.qx = np.concatenate([self.qx, qx])
            self.qy = np.concatenate([self.qy, qy])
            beam_radius_x = self.__q_to_radius(qx, n)
            beam_radius_y= self.__q_to_radius(qy, n)
            self.beam_radius_x = np.concatenate([self.beam_radius_x, beam_radius_x])
            self.beam_radius_y = np.concatenate([self.beam_radius_y, beam_radius_y])
        self.z = np.arange(0, self.cavity_length, self.dz)


    def __q_to_radius(self, q, refractive_index):
        return (self.wavelength / refractive_index / np.absolute((np.imag(1/q))) / np.pi) ** 0.5
    
