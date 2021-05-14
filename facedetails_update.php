<?php 
  ini_set('display_errors', 1);
  ini_set('display_startup_errors', 1);
  error_reporting(E_ALL);

  $datacontext = rtrim($_REQUEST['dataString'],"||");
  $face_details = explode("||", $datacontext);
  $data_string1 = array();

  $url="http://$_SERVER[HTTP_HOST]";
  //output_folder_path = '/var/www/html/cropped_faces/' + filename.replace('.jpg','')
  $output_folder_path = '/var/www/html/cropped_faces/';
  foreach($face_details as $key => $faceseq)
  {

    if($faceseq!="")
    {
        
      $datas = explode("|", $faceseq);

      $arg1 = $datas[0];      #image src
      $arg2 = $datas[1];      #input text label 
      $arg3 = $datas[2];      #text label
      $arg4 = $datas[3];      #id
      
   
      
      if($arg3 == "Unknown Person" or $arg2!=$arg3)
      {
         
          $arg1 = str_replace($url, '/var/www/html', $arg1);
          $arg2 = '"'.$arg2.'"'; 
          $arg3 = '"'.$arg3.'"';
          //$arg1 = "http://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]' class='face_img";
          $commandline_ben = '/home/kanalytics/tmp/deepspeech-venv/bin/python /home/kanalytics/tensorflow1/models/research/object_detection/face_similarity_search_org.py -i '.$arg1.' -n '.$arg2.' -u '.$arg3;

          
         $output = exec($commandline_ben); 
        //   $output1 = str_replace(" ", "_", $output);
        //   $folder_name = substr($arg1,28,-20) ;
        //   echo $newname =  $output_folder_path.$folder_name.$output1.".jpg";
          
        //   if($output1 != 'Unknown_Person'){
        //   rename($arg1, $newname);
        // }

          $data_string1[]= $output."|".$arg4; 
      
   
      } 

    }
  
  } 
  // if($data_string1 != ''){
  //    echo  implode("||",$data_string1);
  // }

  echo  implode("||",$data_string1);
  //echo $arg2;

 
 
	
?>
 