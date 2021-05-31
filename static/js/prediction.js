let out=""
function loadDoc(data) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        console.log(this.responseText)
        if (this.readyState == 4 && this.status == 200) {
            out=JSON.parse(this.responseText).message
            document.getElementById("demo").innerHTML = ` Result => ${out}`;
        }
    };
    xhttp.open("POST", "http://127.0.0.1:5000/.", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(`id=${data}`);
}
var myForm=""
let ouput_data=[]
function sub(e){
    ouput_data=[]
    e.preventDefault();
    console.log("Done")
    myForm = document.getElementById('form_id');
    for(let i=0;i<11;i++){
        ouput_data.push(myForm.elements[i].value)
    }
    senddata(ouput_data)
}
function senddata(dat){
    let temp="["+dat.toString()+"]"
    loadDoc(temp)

}
