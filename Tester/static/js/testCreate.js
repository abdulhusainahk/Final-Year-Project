
window.onload=function(){
form = document.getElementById('test');
form.addEventListener('submit',(event)=>{
    var code = document.getElementById('code').value;
    var flag = true;
    for(let i of tests){
        console.log(i, code)
        if(i.pk == code)
        {
            flag = false;
            break;
        }
    }
    if(!flag)
    {
        alert("Test code already exists");
        event.preventDefault();
    }
})
}
