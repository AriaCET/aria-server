function addit()
{
    var channel_id = $('#inputchannelid').val();
    var channel_name = $('#inputchannelname').val();
    $.post('/addchannel/',{channelid:channel_id ,channelname:channel_name});
    $('#SpeakersInChannelBlock').html(" ");
    setTimeout(
	function(){
	    $('#main_block').load('/channelmanager');
	}
	,500);
}
function removeFromChannel(speaker, channel){
    $.post('/removefromchannel/',{clientid:speaker,groupid:channel});
    setTimeout(
	function(){
	    editChannel(channel);
	}
	,500);
}
function addToChannel(speaker, channel){
    $.post('/addtochannel/',{clientid:speaker,groupid:channel});
    setTimeout(
	function(){
	    editChannel(channel);
	}
	,500);    
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
    $.post('/removechannel/',{channel:channelid});
    setTimeout(
	function(){
	    $('#main_block').load('/channelmanager');
	}
	,500);
}
function reloadDialplan(){
    $.get('/reloaddialplan/');
}
