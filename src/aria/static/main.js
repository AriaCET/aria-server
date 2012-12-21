function addChannel(){
    
	if( $('#inputchannelid').val() && $('#inputchannelname').val() ) {
		if($('#inputchannelid').val() >= 500 && $('#inputchannelid').val() <=600) {
			    var channel_id = $('#inputchannelid').val();
			    var channel_name = $('#inputchannelname').val();
			    //todo: add form validation.
			    $.post('/addchannel/',{channelid:channel_id ,channelname:channel_name},
				   function(data){
				   		if(data !="Done.") alert(data);
				       //todo: check for server errors.
				       channelManager();
				   });    
		} else {
			alert('Channel Number should be in the range 500-600');
		}
	} else {
		alert('Field(s) empty!');
	}
}
function addSpeaker()
{
    if( $('#inputspeakernumber').val()) {
    	if( $('#inputspeakername').val() ) {
			if($('#inputspeakernumber').val() >= 100 && $('#inputspeakernumber').val() <=300) {
				    var speaker_number = $('#inputspeakernumber').val();
				    var speaker_name = $('#inputspeakername').val();
			    	var speaker_ip = $('#inputspeakerip').val();
			   		//todo: add form validation.
			    	$.post('/addspeaker',{number:speaker_number,name:speaker_name,ip:speaker_ip},
					   function(data){
				    	   //todo: check for server errors.
				    	   if(data !="Done.") alert(data);
				    	   speakerManager();
				   	});
			}else {
				alert('Speaker Number should be in the range 100-300');
			}
		}else {
			alert('Name field empty!');
		}
	}else {
		alert('Number field empty!');
	}

}
function changePassword(){
	if ( $('#password').val() ){
		if ( $('#password').val() == $('#rpassword').val() ) {
			var password_val = $('#password').val();
			var rpassword_val = $('#rpassword').val();
			$.post('/changepassword',{password:password_val,rpassword:rpassword_val},
				function(data){
					if(data !="Done.") alert(data);
					//todo: check for server errors.
					speakerManager();
			});
		}else{
			alert('Passwords do not match !');
		}
	}else{
		alert('Empty password is not Perminted!');
	}
}

function removeFromChannel(speaker, channel){
    $.post('/removefromchannel/',{clientid:speaker,groupid:channel},
	   function(data){
	   		if(data !="Done.") alert(data);
	       //todo: check for server errors.
	       editChannel(channel);   
	   });
}
function addToChannel(speaker, channel){
    $.post('/addtochannel/',{clientid:speaker,groupid:channel},
	   function(data){
	   		if(data !="Done.") alert(data);
	       //todo: check for server errors.
	       editChannel(channel);
	   });
}
function editChannel(channel){
    $('#speakers_in_channel_block').load('/listchannel/'+channel);
}
function speakerManager(){
    document.getElementById("speaker_man_link_block").style.fontWeight = 'bold';
    document.getElementById("channel_man_link_block").style.fontWeight = 'normal';
    document.getElementById("speaker_pass_man_link_block").style.fontWeight = 'normal';   
    $('#main_block').load('/listspeakers');
}
function channelManager(){
	document.getElementById("channel_man_link_block").style.fontWeight = 'bold';
	document.getElementById("speaker_man_link_block").style.fontWeight = 'normal';
    document.getElementById("speaker_pass_man_link_block").style.fontWeight = 'normal';
	$('#main_block').load('/channelmanager');
}
function passwordManager(){
	document.getElementById("speaker_pass_man_link_block").style.fontWeight = 'bold';
	document.getElementById("channel_man_link_block").style.fontWeight = 'normal';
    document.getElementById("speaker_man_link_block").style.fontWeight = 'normal';	
	$('#main_block').load('/passwordmanager');
}
function deleteChannel(channelid){
    $.post('/removechannel/',{channel:channelid},
	   function(data){
	   		if(data !="Done.") alert(data);
	       //todo: check for server errors.
	       $('#main_block').load('/channelmanager');
	   });
}
function reloadDialplan(){
    $.get('/reloaddialplan/',function(data){
	   		if(data !="Done.") alert(data);
	       //todo: check for server errors.
	   });
}

