
main=document.getElementsByClassName('main')
navbar=document.getElementsByClassName('navbar')
toggler=document.getElementsByClassName('navbar-toggler')
exp=document.getElementsByClassName('exp')
hicon=document.getElementsByClassName('hicon')
toggler[0].addEventListener('click',()=>{
    if(exp[0].style.height=="100%"){
        exp[0].style.height="0vh";
        hicon[0].style.display="none";
        exp[0].style.display="none";
        console.log("cose");
    }
    else{
        exp[0].style.height="100%";
        hicon[0].style.display="block";
        exp[0].style.display="block";
    }
})