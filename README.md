# compilation-he-arc-class
A programming language to make quick css3 animations without touching css.


# Goal
From a html file, and our langage file, create a css file based on the code.

For instance, if I want to move the div when I'm hove with the mouse


```

python3 csscompile.py input.html ourcode.mylang


```




```
FROM "body";


@each(class="button"){

  if @item.data-no-animate != true {
    @animation(name="on_hover_anim"){
      type = "scaling";
      to = "3%";
      backgroundColor = "red";
    }

    @animation(name="on_click_anim"){
      type = "wave";
    }
    
    @if hover{
      start "on_hover_anim";
    }

    @if click{
      start "on_click_anim";
    }
  }

}

===============================================================================
HTML File

<body>

  <div class="button" data-no-animate="true">My Cool Button</div>
  <div class="button">My Cool Button</div>
  <div class="button">My Cool Button</div>
  <div class="button">My Cool Button</div>

  <div id='test'>


  </div>

</body>



```
