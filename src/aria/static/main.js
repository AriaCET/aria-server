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

function addUser()
{
    if( $('#inputusernumber').val()) {
    	if( $('#inputusername').val() ) {
			if($('#inputusernumber').val() > 300 && $('#inputusernumber').val() <500) {
				    var user_number = $('#inputusernumber').val();
				    var user_name = $('#inputusername').val();
			    	var user_ip = $('#inputuserip').val();
			   		//todo: add form validation.
			    	$.post('/adduser',{number:user_number,name:user_name,ip:user_ip},
					   function(data){
				    	   //todo: check for server errors.
				    	   if(data !="Done.") alert(data);
				    	   userManager();
				   	});
			}else {
				alert('Number should be in the range 301-499');
			}
		}else {
			alert('Name field empty!');
		}
	}else {
		alert('Number field empty!');
	}

}

function changeSpeakerPassword(){
	if ( $('#password').val() ){
		if ( $('#password').val() == $('#rpassword').val() ) {
			var password_val = $('#password').val();
			var rpassword_val = $('#rpassword').val();
			$.post('/speakerpassword',{password:password_val,rpassword:rpassword_val},
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

function changePassword(){
	if ( $('#password').val() ){
		if ( $('#password').val() == $('#rpassword').val() ) {
			var username_val = $('#username').val()
			var password_val = $('#password').val();
			var rpassword_val = $('#rpassword').val();
			$.post('/changepassword',{username:username_val,password:password_val,rpassword:rpassword_val},
				function(data){
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
    document.getElementById("change_pass_man_link_block").style.fontWeight = 'normal';
    document.getElementById("user_man_link_block").style.fontWeight = 'normal';
    $('#main_block').load('/listspeakers');
}
function channelManager(){
	document.getElementById("channel_man_link_block").style.fontWeight = 'bold';
	document.getElementById("speaker_man_link_block").style.fontWeight = 'normal';
    document.getElementById("speaker_pass_man_link_block").style.fontWeight = 'normal';
    document.getElementById("change_pass_man_link_block").style.fontWeight = 'normal';
    document.getElementById("user_man_link_block").style.fontWeight = 'normal';
	$('#main_block').load('/channelmanager');
}
function speakerpassword(){
	document.getElementById("speaker_pass_man_link_block").style.fontWeight = 'bold';
	document.getElementById("channel_man_link_block").style.fontWeight = 'normal';
    document.getElementById("speaker_man_link_block").style.fontWeight = 'normal';
    document.getElementById("change_pass_man_link_block").style.fontWeight = 'normal';
    document.getElementById("user_man_link_block").style.fontWeight = 'normal';	
	$('#main_block').load('/speakerpassword');
}
function passwordmanager(){
	document.getElementById("change_pass_man_link_block").style.fontWeight = 'bold';
	document.getElementById("channel_man_link_block").style.fontWeight = 'normal';
    document.getElementById("speaker_man_link_block").style.fontWeight = 'normal';
    document.getElementById("speaker_pass_man_link_block").style.fontWeight = 'normal';
    document.getElementById("user_man_link_block").style.fontWeight = 'normal';	
	$('#main_block').load('/changepassword');
}
function userManager(){
	document.getElementById("user_man_link_block").style.fontWeight = 'bold';
    document.getElementById("speaker_man_link_block").style.fontWeight = 'normal';
    document.getElementById("channel_man_link_block").style.fontWeight = 'normal';
    document.getElementById("speaker_pass_man_link_block").style.fontWeight = 'normal';
    document.getElementById("change_pass_man_link_block").style.fontWeight = 'normal';   
    $('#main_block').load('/adduser');
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
	   		alert(data);
	       //todo: check for server errors.
	   });
}

$(document).ready(function(){
	$('#footer').mouseover(function() {
  		$(this).find('#credits_hidden_block').toggle(true);
	});
	$('#footer').mouseleave(function() {
		$(this).find('#credits_hidden_block').toggle(false);
	});
});