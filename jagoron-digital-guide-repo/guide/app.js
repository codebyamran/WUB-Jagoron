(function(){
var $=function(s,r){return(r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
/* privacy score: counts "Fix" answers, stored nowhere */
var pr=$$('#privrows .row');
function privUpdate(){var fix=0,done=0;pr.forEach(function(r){var c=$('input:checked',r);if(c){done++;if(c.value==='fix')fix++}});
 var box=$('#privscore'),t=$('#privtxt');box.className='score';
 if(!done){t.textContent='mark each line to see it';return}
 var cls=fix<=2?'g':fix<=5?'a':'r',lab=fix<=2?'Good':fix<=5?'Needs attention':'High risk';
 box.classList.add(cls);t.textContent=lab+' ('+fix+' to fix, '+done+' of '+pr.length+' checked)'}
pr.forEach(function(r){$$('input',r).forEach(function(i){i.addEventListener('change',privUpdate)})});
/* device progress */
var dv=$$('.devck');function devUpdate(){var n=dv.filter(function(c){return c.checked}).length;$('#devfill').style.width=(100*n/dv.length)+'%';$('#devtxt').textContent=n+' of '+dv.length+' done'}
dv.forEach(function(c){c.addEventListener('change',devUpdate)});devUpdate();
/* quiz */
var qs=$$('.qc'),answered=0,good=0;
qs.forEach(function(q){var best=+q.getAttribute('data-best'),bs=$$('button',q);
 bs.forEach(function(b,i){b.addEventListener('click',function(){if(q.classList.contains('done'))return;q.classList.add('done');answered++;if(i===best)good++;
  bs.forEach(function(x,k){x.disabled=true;if(k===best)x.classList.add('right');else if(k===i)x.classList.add('wrong')});
  $('#qscore').textContent='Answered: '+answered+' of '+qs.length+(answered===qs.length?'. Best answers: '+good+' of '+qs.length:'')})})});
/* copy / share */
var cp=$('#copy');if(cp)cp.addEventListener('click',function(){var u=location.href.split('#')[0];
 if(navigator.clipboard){navigator.clipboard.writeText(u).then(function(){cp.textContent='Link copied'})}else{cp.textContent=u}});
var sb=$('#shareb');if(sb&&navigator.share){sb.hidden=false;sb.addEventListener('click',function(){navigator.share({title:document.title,url:location.href.split('#')[0]}).catch(function(){})})}
})();
