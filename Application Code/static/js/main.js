let mic = document.getElementById("mic");
let chatareamain = document.querySelector('.chatarea-main');
let chatareaouter = document.querySelector('.chatarea-outer');

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

function showusermsg(usermsg){
    let output = '';
    output += `<div class="you-message">${usermsg}</div>` ;
    chatareaouter.innerHTML += output;
    return chatareaouter;
}

function showchatbotmsg(chatbotmsg){
    let output = '';
    output += `<div class="other-message">${chatbotmsg}</div>`;
    chatareaouter.innerHTML += output;
    // alert( {{txt}});
    return chatareaouter;
}

function chatbotvoice(message){
    const speech = new SpeechSynthesisUtterance();
    // speech.text = "This is test message";
    // alert(message)

    $.ajax({
        url: 'python_file/',
        type: 'get',
        data: {
            msg : message,
                // 'csrfmiddlewaretoken': '{{ csrf_token }}',
        },
        success: function(response){
            showchatbotmsg(response.ReturnAnswer)
            speech.text = response.ReturnAnswer
            window.speechSynthesis.speak(speech);
            console.log("Success !!")
            console.log("message is:" + message)
        }
    });
    // window.speechSynthesis.speak(speech);
    // chatareamain.appendChild(showchatbotmsg(speech.text));
}

recognition.onresult=function(e){
    let resultIndex = e.resultIndex;
    let transcript = e.results[resultIndex][0].transcript;
    chatareamain.appendChild(showusermsg(transcript));
    chatbotvoice(transcript);
    console.log(transcript);
}
recognition.onend=function(){
    mic.style.background="#ff3b3b";
}
mic.addEventListener("click", function(){
    mic.style.background='#39c81f';
    recognition.start();
    console.log("Activated");
})
