from app.common.helpers import print

import io
import os

from PIL import Image, ImageFile
from io import BytesIO

from .appengine.requests_monkeypatch import requests



ImageFile.LOAD_TRUNCATED_IMAGES = True

JPEG = 'jpeg'
WEBP = 'webp'
PNG = 'png'
JPEG2K = 'jpeg2000'

MIME_TYPES = {
  WEBP: 'image/webp', 
  JPEG2K: 'image/jpeg2000' 
}



class ImageOptimizer:
  default_types = [ WEBP, JPEG2K ]
  size_dict = { 'sm': 512, 'md': 640, 'lg': 1024, 'xl': 1280 }



  def default_file_types(self, file_name):
    default_types = list( self.__class__.default_types )
    ret_file_name = str( file_name.split('.')[-1] )

    #JPG and JPEG are same formats but converted to JPEG for API 
    if ret_file_name == 'jpg':
      default_types.append( JPEG )
    else:
      default_types.append( ret_file_name )

    return default_types



  def optimize(self, file_in, intended_file_type, name):
    #create new Bytes stream
    new_img = BytesIO()
    orig_image = BytesIO()

    file_in.save( orig_image, intended_file_type )
    original_file_name = name.split('.')[0]
    
    # Use when migrated to Python 3 and support for JPEG2000 is available
    if( intended_file_type == JPEG2K ):
      file_in.convert("RGBA").save( new_img, intended_file_type, quality_mode='dB', quality_layers=[41] )

    # Optimize PNG images by reducing colors to avoid increasing file size
    if intended_file_type == PNG: 
      optimized_png = file_in.convert( mode='P', palette=Image.ADAPTIVE )
      optimized_png.save( new_img, intended_file_type, optimize = True, compress_level=95 )
      
    # Optimize all other image formats
    else:
      file_in.save( new_img, intended_file_type, optimize = True, compress_level=95 )

    # File name format: <original_file_name>_compressed.<file_type> 
    new_img.name = original_file_name + '_compressed' + '.' + intended_file_type
    
    if new_img.tell() > orig_image.tell():
      return orig_image
    else: 
      return new_img 

  

  def resize_image(self, bytes_image, intended_size):
    img = Image.open( bytes_image )
    original_file_name = str( bytes_image.name.split( '_compressed' )[0] ) 
    final_image = BytesIO()
    
    width = intended_size
    intended_file_type = bytes_image.name.split('.')[-1]
    
    #resize image
    resize_ratio = (width) / float( img.size[0] ) 
    height_size = int( float( img.size[1] ) * float( resize_ratio ) ) 

    resized_img = img.resize( (width, height_size) )
    resized_img.save( final_image, intended_file_type )

    #File Name Format: <original_file_name>_resized_<size>.<file_type> 
    final_image.name = original_file_name + '_resized_' + str(intended_size) + '.' + intended_file_type
    
    print ( 'Resized File Size - ' + str(intended_size)  +  ':' + str( final_image.tell() ) )
    return final_image
    
    
    
  def default_resize(self, bytes_image):
    image_dict = {}
    
    for size in self.__class__.size_dict:
        new_bytes_image = self.resize_image( bytes_image, self.__class__.size_dict[size] )
        image_dict[size] = new_bytes_image

    return image_dict
  	
