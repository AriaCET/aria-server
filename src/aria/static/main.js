function addChannel(){
    
	if( $('#inputchannelid').val() && $('#inputchannelname').val() ) 
	{	if($('#inputchannelid').val() >= 500 && $('#inputchannelid').val() <=600)
		{	    var channel_id = $('#inputchannelid').val();
			    var channel_name = $('#inputchannelname').val();

			    $.post('/addchannel/',{channelid:channel_id ,channelname:channel_name},
				   function(data){
				       //todo: check for server errors.
				       channelManager();
				   });    
		}
		else
		{	alert('Channel Number should be in the range 500-600');
		}
	}
	else
	{	alert('Field(s) empty!');
	}

}
function addSpeaker()
{
    if( $('#inputspeakernumber').val() && $('#inputspeakername').val() ) 
	{	if($('#inputspeakernumber').val() >= 100 && $('#inputspeakernumber').val() <=300)
		{	    var octet = '(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])';
  			    var ip    = '(?:' + octet + '\\.){3}' + octet;
  			    var ipRE  = new RegExp( '^' + ip + '$' );
    			    if( $('#inputspeakerip').val().trim()=='' || ipRE.test( $('#inputspeakerip').val() ))
			    {	var speaker_number = $('#inputspeakernumber').val();
			    	var speaker_name = $('#inputspeakername').val();
			    	var speaker_ip = $('#inputspeakerip').val();
			    	
			    	$.post('/addspeaker',{number:speaker_number,name:speaker_name,ip:speaker_ip},
				   	function(data){
				       	//todo: check for server errors.
				       		speakerManager();
				   	});
			    }
			    else
				{	alert('Invalid IP Address!!');
				}
		}
		else
		{	alert('Speaker Number should be in the range 100-300');
		}
	}
	else
	{	alert('Field(s) empty!');
	}

}
function removeFromChannel(speaker, channel){
    $.post('/removefromchannel/',{clientid:speaker,groupid:channel},
	   function(data){
	       //todo: check for server errors.
	       editChannel(channel);   
	   });
}
function addToChannel(speaker, channel){
    $.post('/addtochannel/',{clientid:speaker,groupid:channel},
	   function(data){
	       //todo: check for server errors.
	       editChannel(channel);
	   });
}
function editChannel(channel){
    $('#speakers_in_channel_block').load('/listchannel/'+channel);
}
function speakerManager(){
    $('#main_block').load('/listspeakers');
}
function channelManager(){
    $('#main_block').load('/channelmanager');
}
function deleteChannel(channelid){
    $.post('/removechannel/',{channel:channelid},
	   function(data){
	       //todo: check for server errors.
	       $('#main_block').load('/channelmanager');
	   });
}
function reloadDialplan(){
    $.get('/reloaddialplan/');
}

