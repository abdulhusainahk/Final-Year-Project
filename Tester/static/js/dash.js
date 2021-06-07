
function load_testCreation() {
				document.getElementById("frame1").style.display="none";
				document.getElementById("content").style.display="block";
     			document.getElementById("content").innerHTML='<object width="100%" height="100%" type="text/html" data="testcreate" ></object>';
			}

function load_studentTest() {
document.getElementById("content").style.display="block";
    document.getElementById("frame1").style.display="none";
    document.getElementById("content").innerHTML='<object width="100%" height="100%"  type="text/html" data="appear" ></object>';
}

function load_history() {
document.getElementById("content").style.display="block";
    document.getElementById("frame1").style.display="none";
    document.getElementById("content").innerHTML='<object width="100%" height="100%"  type="text/html" data="testhistory" ></object>';
}


function submitCode(tests) {
    var userCode = prompt("Please enter test access code:", "access code");
    if(userCode==null)
        return;
    var flag=false;
    for(let i of tests){
        if(i==userCode){
            flag = true;
            break;
        }
    }
    if(!flag)
        alert("No such test !!");
    else
    {
        for(let i of completedTests){
            console.log('i=',i.fields);
            if(i.fields.code==userCode && userName==i.fields.userEmail){
                flag = false;
                //break;
            }
        }
        if(!flag)
            alert("You have already submitted this test !");
        else{
            var f1 = document.getElementById("frame1");
            f1.style.display="block";
            document.getElementById("content").style.display="none";
            f1.data = "appear/" + userCode.toString();
        }
    }

}
if(window.history.replaceState){
		window.history.replaceState(null,null,window.location.href);
	}



