document.addEventListener("DOMContentLoaded",()=>{
  const btn=document.getElementById("generateQuiz");
  if(btn){
    btn.addEventListener("click",()=>{
      document.getElementById("quizContainer").innerHTML="<p>Sample Quiz: What is Regression?</p><ul><li>Prediction method</li><li>Data cleaning</li></ul>";
    });
  }
});