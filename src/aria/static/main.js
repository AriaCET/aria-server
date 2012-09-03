function addit()
{
    var channel_id = $('#inputchannelid').val();
    var channel_name = $('#inputchannelname').val();
    $.post('/addchannel/',{channelid:channel_id ,channelname:channel_name},
	   function(data){
	       $('#SpeakersInChannelBlock').html(" ");
	       $('#main_block').load('/channelmanager');
	   });
}
function removeFromChannel(speaker, channel){
    $.post('/removefromchannel/',{clientid:speaker,groupid:channel},
	   function(data){
	       editChannel(channel);   
	   });
}
function addToChannel(speaker, channel){
    $.post('/addtochannel/',{clientid:speaker,groupid:channel},
	   function(data){
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
	       $('#main_block').load('/channelmanager');
	   });
}
function reloadDialplan(){
    $.get('/reloaddialplan/');
}
