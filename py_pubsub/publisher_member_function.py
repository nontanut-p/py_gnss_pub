import rclpy
import pynmea2  # end mea2
import serial
from rclpy.node import Node
import csv
from tutorial_interfaces.msg import Num    # CHANGE
from math import *

lat_0 = 14.0790659
lon_0 = 100.6014028
earth_radius = 6356752.3142    # meter


def lla2meter( lat, lon ):
  global lat_0, lon_0, earth_radius

#  y = distance( lat_0, lon_0, lat, lon_0 )
  y = (lat - lat_0) * pi/180.0 * earth_radius

#  x = distance( lat_0, lon_0, lat_0, lon )
  if lon > lon_0:
    sign = 1.0
  else:
    sign = -1.0
  a = cos(lat_0* pi/180.0)**2 * sin((lon-lon_0)*0.5* pi/180.0)**2
  x = 2 * atan2(sqrt(a), sqrt(1-a)) * earth_radius
  
  x = sign*abs(x)
  return x,y

serialPort = serial.Serial(port="/dev/ttyACM0", baudrate=115200)

class MinimalPublisher(Node):
    altitude = 0
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Num, 'topic', 10)     # CHANGE
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
    
    def timer_callback(self):
        global altitude
        msg = Num()                                           # CHANGE
        serialString = ""
        if serialPort.in_waiting > 0:
            try : 
              serialString = serialPort.readline().decode("Ascii")
     
              #print(serialString)
              if "$GPGGA" in serialString:
      #           print('test found GPGGA',positionData)
                  try:
                      positionData = pynmea2.parse(serialString)
                      altitude = float(positionData.altitude) 
                  except:
                      pass
  #$GNRMC,143909.00,A,5107.0020216,N,11402.3294835,W,0.036,348.3,210307,0.0,E,A*31               
              if "$GNRMC" in serialString:
                  
      #           print('test found GPGGA',positionData)
                  try:
                      positionData = pynmea2.parse(serialString)
                      #print( spd_over_grnd) ,knot /  1.9438  is equal m/s 
                      #print (true_course) , degree  วัดตามเข็มจาำก ทิศเหนือ   N == 0  
                      
                      msg.lat = float(positionData.latitude) 
                      msg.lon = float(positionData.longitude)
                      x,y = lla2meter(msg.lat, msg.lon)
                      msg.x = x 
                      msg.y = y
                      print('x', msg.x , 'y' , msg.y)
                      self.x = msg.x
                      self.y = msg.y
                      msg.dis = sqrt(x**2 + y**2)
                      self.dis = msg.dis
                      self.lat = msg.lat
                      self.lon = msg.lon 
                      msg.velo = float(positionData.spd_over_grnd) /1.9438
                      msg.dir = float(positionData.true_course)
                      self.velo = msg.velo 
                      self.dir = msg.dir 
                      self.alt = altitude
                      msg.alt = altitude
                  except:
                      passs
            except:
                print('Error')
                pass  
        if msg.lat > 0 :
            
            self.publisher_.publish(msg)
            self.get_logger().info('Latitude "%f" ' % msg.lat +  'Longitude "%f" ' % msg.lon + 'Altitude "%f" ' % msg.alt +  'Velocity "%f" ' % msg.velo + 'True course "%f" ' % msg.dir )  

       
        
        # X , Y , ->   and Heading , Velo

    
       
def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()




'''
float64 lat
float64 lon
float64 alt
float64 velo
float64 x
float64 y
float64 dis
py_pubsub.publisher_member_function
#print(msg.track)
#print( spd_over_grnd) ,knot /  1.9438  is equal m/s 
#print (true_course) , degree  วัดตามเข็มจาำก ทิศเหนือ   N == 0  

#<RMC(timestamp=datetime.time(14, 39, 9), status='A', lat='5107.0020216', lat_dir='N', lon='11402.3294835', lon_dir='W', spd_over_grnd=0.036, true_course=348.3, datestamp=datetime.date(2007, 3, 21), mag_variation='0.0', mag_var_dir='E') data=['A']>

'''