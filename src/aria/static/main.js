function addChannel(){
    var channel_id = $('#inputchannelid').val();
    var channel_name = $('#inputchannelname').val();
    //todo: add form validation.
    $.post('/addchannel/',{channelid:channel_id ,channelname:channel_name},
	   function(data){
	       //todo: check for server errors.
	       channelManager();
	   });
}
function addSpeaker(){
    var speaker_number = $('#inputspeakernumber').val();
    var speaker_name = $('#inputspeakername').val();
    var speaker_ip = $('#inputspeakerip').val();
    //todo: add form validation.
    $.post('/addspeaker/',{number:speaker_number,name:speaker_name,ip:speaker_ip},
	   function(data){
	       //todo: check for server errors.
	       speakerManager();
	   });
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
    $('#SpeakersInChannelBlock').load('/listchannel/'+channel);
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
