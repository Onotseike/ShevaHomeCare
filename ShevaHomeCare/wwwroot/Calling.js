//Constants
var demoAPIKey = 'a78e3020-0882-423b-8a2e-d429455316e2';
var prodAPIKey = '3216b5dd-c8b3-45c4-b7f3-e0912913d78d';


var sinchUser = $('h4#usernameSinch').text();
var userToCall = 'Jamie';
var callType = 'Video';
var sinchLoginObject = { username: sinchUser, password: "HelloWorld" };

var voiceCallListener;
var call;

var handleError = function (error) {
    console.log(error.message);
};

//Sinch Client Creation and Logging In
var sinchClient = new SinchClient({
    applicationKey: demoAPIKey,
    capabilities: { calling: true, video: true },
    supportActiveConnection: true
    //onLogMessage: function (message) {
    //    console.log(message.message);
    //}
});

sinchClient.startActiveConnection();


sinchClient.start(sinchLoginObject,
    function () {
        //activateSinchClient();
        console.log("Logged in!");
        //offline.style.display = 'none';
        //online.style.display = 'block'; 
        console.log(sinchUser);
        console.log("Recipient is " + userToCall);
        
    });


sinchClient.newUser(sinchLoginObject, function (ticket) {
    sinchClient.start(ticket, function () {
        
        console.log("Created New user");
        console.log("Logged in as A New User!");
        //offline.style.display = 'none';
        //online.style.display = 'block';
        console.log(sinchLoginObject.username);
        
    }).fail(handleError);
});

var userCallClient = sinchClient.getCallClient();


//Calling

//Making Voice OutGoing Calls

voiceCallListener = {
    onCallProgressing: function (call) {
        $('audio#ringback').prop("currentTime", 0);
        $('audio#ringback').trigger("play");

        console.log(call.userId + " is ringing");
    },
    onCallEstablished: function (call) {
        $('audio#ringback').trigger("pause");
        $('audio#ringtone').trigger("pause");

        //var phone = document.getElementById("shakeAnim");
        //phone.style.display = 'none';

        
        if (callType === 'Voice')
        {
            $('audio#incomingAudio').attr('src', call.incomingStreamURL);
            $('video#outgoingVideo').attr('src', '');
            $('video#incomingVideo').attr('src', call.incomingStreamURL);
        } else {
            $('audio#incomingAudio').attr('src', '');
            $('video#incomingVideo').attr('src', call.incomingStreamURL);
            $('video#outgoingVideo').attr('src', call.outgoingStreamURL);
        }


        //Report call stats
        var callDetails = call.getDetails();
        console.log("Answered at " + callDetails.establishedTime
            + " " + new Date(callDetails.establishedTime));
    },
    onCallEnded: function (call) {
        $('audio#ringback').trigger("pause");
        $('audio#ringtone').trigger("pause");
        $('audio#incomingVoice').attr('src', '');

        //var phone = document.getElementById("shakeAnim");
        //phone.style.display = 'none';

        $('video#outgoingVideo').attr('src', '');
        $('video#incomingVideo').attr('src', '');

        $("button#voiceCallBtn").prop("disabled", false);
        $("button#videoCallBtn").prop("disabled", false);

        $("button#answer").prop("disabled", false);
        $("button#hangup").prop("disabled", false);

        $(this).prop("disabled", false);
        $('button#answerCallBtn').prop("disabled", false);
        $('button#videoCallBtn').prop("disabled", false);
        $('button#voiceCallBtn').prop("disabled", false);

        console.log("CALL ENDED!");
        $('div#callModal').modal('hide');
        //Report call stats
        var callDetails = call.getDetails();

        $('input#startTime').val(callDetails.startedTime);
        $('input#stopTime').val(callDetails.endedTime);
        $('input#duration').val(callDetails.duration);
        $('input#endCause').val(call.getEndCause());

        //$('input#sessionTherapistId').val(therapistUsername);
        // $('input#clientId').val(call.fromId);
        //  $('input#subType').val(clientSubcription);
        //$('div#myModal').modal('show');
        if (call.error) {
            console.log('Failure message: ' + call.error.message);
        }
    }
};



userCallClient.addEventListener({
    onIncomingCall: function (incomingCall) {
        //Play some groovy tunes 
        $("button#videoCallBtn").prop("disabled", true);
        $("button#voiceCallBtn").prop("disabled", true);


        $('div#callModal').modal('setting', 'closable', false).modal('show');
        //var phone = document.getElementById("shakeAnim");
        //phone.style.display = 'block';

        $('audio#ringtone').prop("currentTime", 0);
        $('audio#ringtone').trigger("play");
        callType = 'Video';
        console.log("Incoming call from " + incomingCall.fromId);
        //$('h4#receiptientSinch').text(incomingCall.fromId);
        //$('p#callingReceiptient').text(incomingCall.fromId);
        //$('input#clientId').val(incomingCall.fromId);
       
        
        call = incomingCall;
        call.addEventListener(voiceCallListener);
       
    }
});


$('button#videoCallBtn').click(function(event) {
    event.preventDefault();
    if (userToCall !== '') {
        $(this).prop("disabled", true);
        $('button#voiceCallBtn').prop("disabled", true);

        callType = 'Video';
        console.log("Calling " + userToCall);
        //$('input#clientId').val(userToCall);
        call = userCallClient.callUser(userToCall);
        call.addEventListener(voiceCallListener);

    }
});


$('button#voiceCallBtn').click(function (event) {
    event.preventDefault();
    if (userToCall !== '') {
        $(this).prop("disabled", true);
        $('button#videoCallBtn').prop("disabled", true);

        callType = 'Voice';
        console.log("Calling " + userToCall);
        //$('input#clientId').val(userToCall);
        call = userCallClient.callUser(userToCall);
        call.addEventListener(voiceCallListener);

    }
});

$('button#answerCallBtn').click(function (event) {
    event.preventDefault();
    if (call === undefined) {
        $(this).prop("disabled", false);
        $('button#endCallBtn').prop("disabled", false);
        $('button#videoCallBtn').prop("disabled", false);
        $('button#voiceCallBtn').prop("disabled", false);
    }
    else
    {
        $(this).prop("disabled", true);
        $('button#endCallBtn').prop("disabled", false);
        $('button#videoCallBtn').prop("disabled", true);
        $('button#voiceCallBtn').prop("disabled", true);


        try {
            call.answer();
        } catch (e) {
            handleError(e);
        } 
    }
});

$('button#endCallBtn').click(function (event) {
    event.preventDefault();
    if (call) {
        $(this).prop("disabled", false);
        $('button#answerCallBtn').prop("disabled", false);
        $('button#videoCallBtn').prop("disabled", false);
        $('button#voiceCallBtn').prop("disabled", false);

        $('audio#ringtone').trigger("pause");
        $('audio#ringtone').prop("currentTime", 0);


        console.log("You hung up the call");
        call.hangup();
        call = null;
    }
});


