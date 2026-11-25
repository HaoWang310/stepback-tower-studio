// Mesh Master File
global_settings { assumed_gamma 2.2 }
#declare scal=.95;


#include "colors.inc"

#declare bb=.4;

background {color White} // background color

#declare stereo =0;
camera {
	location <0,0,-4>+stereo*<.1,0,0>

 	right x*image_width/image_height    
	 angle 40 look_at 0
 }

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

#declare tr=0.4; // 0.2
#declare meshcolor1=rgb <0.562195, 0.775018, 0.672325>;
#declare meshcolor2=rgb <0.955589, 0.830178, 0.711719>;




#declare spherecolor = rgb <0.76, .76, 0.8>/4;  


#declare rodcolor1 =  rgb <0.476341, 0.146953, 0.137403>;  
#declare rodcolor2 = rgb <0.942502, 0.898717, 0.869791>;






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
	ambient .3
	diffuse .2
	specular .1 
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


#declare linerad=0.003/scal;
#declare sphererad=0.006/scal;

// include generated file

#include "dummy.pov"

#declare fundpiece1 = object{
union {

	object {MESHtriangles
			texture { 
						mesh_texture2
					}
					interior_texture { 
						mesh_texture1
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

//	#declare dx=27.8136;
//	#declare dy=17.3992;
//	
//	
//	#declare fundpiece2= union{
//	object{fundpiece1}
//	object{fundpiece1 translate <dx,0,0>} 
//	object{fundpiece1 translate <-dx,0,0>} 
//	}
//	
//	#declare fundpiece3= union{
//	object{fundpiece2}
//	object{fundpiece2 translate <0,dy,0>} 
//	object{fundpiece2 translate <0,-dy,0>} 
//}

object{
	object{fundpiece1}
	scale scal
	rotate <-90,-60,0>
	rotate <-30,0,0>
	translate <.1,.15,0>
}

	


