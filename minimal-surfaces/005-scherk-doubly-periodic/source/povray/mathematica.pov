// Mesh Master File

global_settings { assumed_gamma 2.2 }
#declare scal=.9;

#include "colors.inc"



background {color rgb 1} // background color

#declare stereo =0;
camera {
	location <0,0,-4>+stereo*<.1,0,0>

 	right x*image_width/image_height    
	 angle 40 look_at 0
 }

#declare bb=.8;

 light_source { 
	 <5,0,-20>
 	color  rgb <1,bb,bb>
//	shadowless
 }
 light_source { 
 	<0,5,-20>
 	color  rgb <bb,bb,1>
//	shadowless
 }
 light_source { 
 	<0,-5,-20>
	 color  rgb <bb,1,1>
//	shadowless
 }
 light_source { 
 	<-5,0,-20>
	 color  rgb <1,1,bb>
//	shadowless
 }


// texture parameters


#declare meshcolor1=rgb <0.000000, 0.611808, 0.528390>;
#declare meshcolor2=rgb <0.738212, 0.464737, 0.377568>;




//#declare meshcolor1=rgbt <0.719463, 0.381231, 0.458305,.2>;
//#declare meshcolor2=rgbt <0.303410, 0.607736, 0.719463,.2>;
//
//

#declare spherecolor = rgb <0.76, .76, 0.8>/4;  


#declare rodcolor1 =  rgb <0.784085, 0.735470, 0.727169>;  
#declare rodcolor2 = rgb <0.315908, 0.296315, 0.331823>;




#declare RodFinish  =
finish {
    ambient 0.25
    brilliance 3
    diffuse 0.5
    metallic
    specular 0.70
    roughness 1/80
}


#declare SphereFinish = 
finish {
	specular 1
	phong 1
	roughness .1
	metallic
} 


#declare MeshFinish =
finish {
	ambient .2
	diffuse .3
	specular .05 
	roughness 0.16 
}
#declare mesh_texture1 = texture { 
			pigment {
				color meshcolor1
			}
			finish {
   				MeshFinish
 			}
}

#declare mesh_texture2 = texture {
pigment {
				color meshcolor2 
			}
			finish {
   				MeshFinish
 			}
}

// thicknesses of spheres and rods

#declare linerad=0.001/scal;
#declare sphererad=0.002/scal;

// include generated file

#include "dummy.pov"

#declare fundpiece = object{
union {

	object {MESHtriangles
		texture { 
					mesh_texture1
				}
				interior_texture { 
					mesh_texture2
				}
		}
	object {MESHspheres
		pigment {spherecolor }    
				finish{SphereFinish} 
		}
	object {MESHhorlines
		pigment {rodcolor1}     
				finish{RodFinish} 
		}
	object {MESHverlines
		pigment {rodcolor2}     
				finish{RodFinish} 
		}

}
}


	object{fundpiece 
	scale scal
	rotate <90,45,0>
	rotate <-30,0,0>
	translate <0,.1,0>
	
}