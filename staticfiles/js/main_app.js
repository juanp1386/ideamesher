
var tree_buttons = document.getElementsByClassName('tree_link');
var tree_buttons_ids = [];
var svg =  document.getElementById('tree_svg');
var x_max = 0;
var y_max = 0;


for (var i = 0; i < tree_buttons.length; i++) {
    tree_buttons_ids[i] = tree_buttons[i].id;
    var x = tree_buttons[i].getElementsByClassName('tree_button_group')[0].getElementsByClassName('tree_button')[0].getAttribute("x");
    var y = tree_buttons[i].getElementsByClassName('tree_button_group')[0].getElementsByClassName('tree_button')[0].getAttribute("y");
    if(parseInt(x)>x_max){
      x_max=x;
    }
    if(parseInt(y)>y_max){
      y_max=y;
    }
}

x_max=parseInt(x_max)+60;
y_max=parseInt(y_max)+60;

console.log("x_max = "+x_max);
svg.setAttribute("width",x_max);
svg.setAttribute("height",y_max);

for (var i = 0; i < tree_buttons_ids.length; i++) {
    var tree_button = tree_buttons_ids[i];

    svg.appendChild(document.getElementById(tree_button));
}
