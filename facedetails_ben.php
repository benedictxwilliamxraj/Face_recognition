
<?php 
//error_reporting(1);
header('Access-Control-Allow-Origin: *');
//var_dump($_REQUEST);
$commandline = '/home/kanalytics/tmp/deepspeech-venv/bin/python /home/kanalytics/create_face_data_from_images/face_detect_rec_server.py '.$_REQUEST['path'];
// $commandline_ben = '/home/kanalytics/tmp/deepspeech-venv/bin/python /home/kanalytics/tensorflow1/models/research/object_detection/face_similarity_search_org.py '
$commandline = '/home/kanalytics/tmp/deepspeech-venv/bin/python /home/kanalytics/tensorflow1/models/research/object_detection/face_logo_detect_rec_server1.py '.$_REQUEST['path'];


$output = exec(escapeshellcmd($commandline)); 
$faces=explode('|',$output);

//$url='http://115.112.153.221/';
$url="http://$_SERVER[HTTP_HOST]/";




foreach($faces as $face)
{
	if($face != '')
	{		
		if(stripos($face,'Logo'))
		{
			$logos=explode(',',str_replace('[Logo]','',$face));

			foreach($logos as $logo)
				{
					if($logo!='')
					{
						$logofname=explode(':',trim($logo));
						$confid=trim(str_replace('%','',$logofname[1]));
						if($confid>75)
						{
							echo "<div style='float:left; width:auto;'>";
							echo "<img src='".$url."/bank_logo/".str_replace(' ','_',$logofname[0]).".jpg' style='width:100px; margin:5px;'><br>";
							echo "<span style='margin:5px; margin-top:0px;' class=''>";
							echo $logo;
							echo "</span>";
							echo "</div>";
						}
					}
				}
		}
		else{

	
			//echo $str= preg_replace('/\W\w+\s*(\W*)$/', '$1', ucwords(str_replace('_',' ',str_replace('.jpg','',$flastname))));
			echo "<div class='content' style='float:left; width:auto;'>";
			
			echo "<img src='" .str_replace('/var/www/html/', $url,str_replace('|', '',$face))."' class='face_img' style='width:100px; margin:5px;'><br>";   #printing 
			//echo "<img src='http://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]' class='face_img' style='width:100px; margin:5px;'><br>";
			$facename=explode('/',$face);
			$flastname=$facename[sizeof($facename) -1];
			echo "<span style='margin:5px; margin-top:0px;' id='".str_replace(".jpg","",$flastname)."' class='face_label'>";           #have to id over here
			echo $str= preg_replace('/\W\w+\s*(\W*)$/', '$1', ucwords(str_replace('_',' ',str_replace('.jpg','',$flastname))));
			echo "</span>";
			echo "<br>";
			echo "<span style='margin:5px; margin-top:0px;'>";
			//echo "<input class='face_label' type='hidden' id='".str_replace(".jpg","",$flastname)."' name='face_label[]' value='".$str."' />";					#Text
			echo "<input class='input_face_label' type='text'  name='input_face_label[]' id='".str_replace(".jpg","",$flastname)."+i' value='".$str."' />";		#INPUT TEXTBox value='".$str."'

	    	/*													 	
			echo "<input class='face_label_url' type='hidden' id='h_".$flastname."' name='face_label_url[]' value='" .str_replace('/var/www/html/','http://192.168.1.74/',str_replace('|', '',$face))."' />";*/
			   
			echo "</span>";
			echo "</div>";
		}
		
	}
}	

	?>

	
<div>
	<input type='submit' name='submit'  value='Submit' class='save_face_btn'>
</div>


 <script type = "text/javascript" 
         src = "https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js">
      </script>



<script type="text/javascript">

$(document).ready(function(){
	var datastring ="";
	$('.content').each(function(){
		var images = $(this).find('.face_img').attr('src');
			//var images = $(".face_img").attr('src');   
			var term =  $(this).closest('div.content').find(".input_face_label").val();
			var term_label = $(this).closest('div.content').find(".face_label").text();
			var term_id = $(this).closest('div.content').find(".face_label").attr('id');
			datastring += images+"|"+term+"|"+term_label+"|"+term_id+"||";
     	 
    	 });
		//alert(datastring);

$.ajax({ url: "../facedetails_update.php?",
        //context: document.body,
        type:"GET",
        data:"dataString="+datastring,
        success: function(data){
        	var new_data = data.split("||");
			 $.each( new_data, function( key, value ) { 
			var res = value.split("|");  
			
			$("#"+res[1]).html(res[0]);
			$("#"+res[1]).closest('div.content').find(".input_face_label").val(res[0]);
          	
        });
		}
	});
});




$(document).ready(function(){


	$(".save_face_btn").click(function(){ 
		var datastring="";
		 $('.content').each(function() {
			var images = $(this).find('.face_img').attr('src');
			//var images = $(".face_img").attr('src');   
			var term =  $(this).closest('div.content').find(".input_face_label").val();
			if(term == ""){
				alert('Kindly Fill the name.'); 
				return;
			}
			var term_label = $(this).closest('div.content').find(".face_label").text();
			var term_id = $(this).closest('div.content').find(".face_label").attr('id');
			datastring += images+"|"+term+"|"+term_label+"|"+term_id+"||";
     	 
    	 });
		 
		$.ajax({
			type:"GET",
			cache:false,
			url:"../facedetails_update.php?",
			data: "dataString="+datastring,    
			success: function(data){

				var new_data = data.split("||");
			 	$.each( new_data, function( key, value ) { 
				 	var res = value.split("|"); 
			   		$("#"+res[1]).html(res[0]);
				}); 
			}
		});    
		
	});
});

</script>