
GAS_DENSITY = 2.858
ONE_MPH = 0.44704

import rospy
from pid import PID
from yaw_controller import YawController
from lowpass import LowPassFilter


class Controller(object):
    def __init__(self, **kwargs):
        # TODO: Implement
        # Fixed parameters
<<<<<<< HEAD

        self.vehicle_mass = kwargs['vehicle_mass']
        self.fuel_capacity = kwargs['fuel_capacity']
        self.brake_deadband = kwargs['brake_deadband']
        self.decel_limit = kwargs['decel_limit']
        self.accel_limit = kwargs['accel_limit']
        self.wheel_radius = kwargs['wheel_radius']
        self.wheel_base = kwargs['wheel_base']
        self.steer_ratio = kwargs['steer_ratio']
        self.max_lat_accel = kwargs['max_lat_accel']
        self.max_steer_angle = kwargs['max_steer_angle']

        # To be Updated in each cycle
        self.twist_command = None
        self.current_velocity = None
        self.enabled = True
        self.sample_time = 1/50 # initial value, gets updated in loop


        self.speed_PID = PID(1.0, 0.0, 0.0) # Dummy values


        #initial control values	
        self.steer = 0.0

        self.yaw_ctrl = YawController(self.wheel_base,
                                      self.steer_ratio,
                                      0,
                                      self.max_lat_accel,
                                      self.max_steer_angle) # Set the min_speed as 0

        self.LPF = LowPassFilter(0.96, 1.0)

    def get_speed_control_vector(self, speed_command):
        #default control behavior, don't do anything
        throttle = 0.0
        brake = 0.0

        if speed_command > 0.01:
            throttle = max(min(speed_command, 1.0), 0.0)
            brake = 0.0
        elif speed_command < 0.0:
            throttle = 0.0
            brake = max(min(abs(speed_command), 1.0), 0.0)
        return throttle, brake

    def control(self, target_v, yaw_angle, actual_v, dbw_status):
        # TODO: Change the arg, kwarg list to suit your needs
        # If we drive slower than the target sppeed, we push the gas pedal (throttle), othwise not
        speed_error = target_v - actual_v
        speed_command =  self.speed_PID.step(speed_error, self.sample_time)
        throttle_command, brake_command = self.get_speed_control_vector(speed_command)
        yaw_angle = self.LPF.filt(yaw_angle)
        # self.steer = self.yaw_ctrl.get_steering(actual_v, yaw_angle, actual_v) 
        steer = self.yaw_ctrl.get_steering(actual_v, yaw_angle, actual_v)

        # Return throttle, brake, steer
        return throttle_command, brake_command, steer
