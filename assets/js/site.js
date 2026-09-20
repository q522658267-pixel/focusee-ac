/* FOCUSEE site scripts */
(function(){
  var b=document.getElementById('burger'), n=document.getElementById('navmain');
  if(b&&n){ b.addEventListener('click',function(){ n.classList.toggle('open'); }); }
  document.querySelectorAll('.has-sub > a').forEach(function(a){
    a.addEventListener('click',function(e){
      if(window.innerWidth<=900){ e.preventDefault(); a.parentNode.classList.toggle('open'); }
    });
  });

  /* product filters */
  var fw=document.getElementById('filters');
  if(fw){
    fw.addEventListener('click',function(e){
      var btn=e.target.closest('button'); if(!btn) return;
      var f=btn.dataset.f;
      fw.querySelectorAll('button').forEach(function(x){ x.classList.toggle('on', x===btn); });
      var groups=document.querySelectorAll('.pgroup');
      if(groups.length){
        groups.forEach(function(g){ g.style.display = (f==='all'||g.dataset.cat===f)?'':'none'; });
      }
      var grid=document.getElementById('grid');
      if(grid){
        grid.querySelectorAll('.card').forEach(function(c){
          var ok = f==='all' || (c.dataset.cat===f);
          c.style.display = ok?'':'none';
        });
      }
    });
  }

  /* product gallery — keeps <picture><source type=webp> in sync with <img> */
  var m=document.getElementById('pdmain');
  if(m){
    var wrap=m.parentNode, sp=(wrap && wrap.tagName==='PICTURE') ? wrap.querySelector('source') : null;
    document.querySelectorAll('.pd-thumbs button').forEach(function(b){
      b.addEventListener('click',function(){
        document.querySelectorAll('.pd-thumbs button').forEach(function(x){x.classList.remove('on');});
        b.classList.add('on');
        var w=b.getAttribute('data-webp');
        if(sp){
          if(w){
            /* re-attach if a previous switch had to detach the webp source */
            if(!sp.parentNode) wrap.insertBefore(sp, m);
            sp.setAttribute('srcset', w);
          } else if(sp.parentNode){
            /* this image has no webp sibling: drop the source or the old one keeps winning */
            sp.parentNode.removeChild(sp);
          }
        }
        m.src=b.dataset.src;
      });
    });
  }

  /* header shadow on scroll */
  var hd=document.querySelector('header');
  if(hd){ window.addEventListener('scroll',function(){
    hd.style.boxShadow = window.scrollY>10 ? '0 6px 24px rgba(10,25,41,.08)' : 'none';
  }); }
})();
