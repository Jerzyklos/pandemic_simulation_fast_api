//GLOBAL VARIABLES
var streets_number = 1;
var board_size = 500; 
var occupied_percent_beginning = 10;
var slow_down_percent = 5;
var v_max = 3;
var s_number = [2];
var b_number = [3];
var average_velocity_data = [];
drawAverageVelocityChart();

var traffic_lights_img = new Image();   
traffic_lights_img.src = 'lights.png'; 
var id_simulation = 0;
var id_traffic_lights = 0;
var board = [];
var traffic_lights = 0;
var how_many_cars=0;

var simulation_speed = 400;
var traffic_light_speed_step = 500;
var steps_till_traffic_light_change = 0;


class Cell {
    constructor(is_occupied){
        this.is_occupied = is_occupied;
        if(is_occupied) this.v = 1;
        else this.v = 0;
    }
    changeV(new_v){
        this.v = new_v;
    }
}

function initializeSimulation(){
    stopSimulation();
    console.log("inicjalizuje");

    var new_speed = document.getElementById("simulation_speed").value;
    simulation_speed = parseInt(new_speed);

    var new_traffic_light_speed = document.getElementById("traffic_light_speed").value;
    traffic_light_speed_step = parseInt(new_traffic_light_speed)/10;

    streets_number = document.getElementById("streets_number").value[0];
    
    RefreshOccupiedPercent();

    var rows = parseInt(streets_number)*2;
    var cols = 10*(parseInt(streets_number)+1)+parseInt(streets_number);

    drawBackground();

    board = MakeAndInitializeBoard(rows, cols, occupied_percent_beginning);
    drawBoard(rows, cols, board);
    
    //0 to zielone światło w poziomie, 1 to zielone w pionie
    traffic_lights = 0;
}

function MakeAndInitializeBoard(rows, cols, percent){
    var board = new Array(rows);
    var cars = 0;
    for(var i = 0; i < rows; i++){
        board[i] = new Array(cols);
    }
    for(var i = 0; i < rows; i++){
        for(var j = 0; j < cols; j++){
            if(Math.random()*100<=percent){ 
                board[i][j] = new Cell(true);
                cars++;
            }
            else board[i][j] = new Cell(false);
        }
    }
    how_many_cars = cars;
    RefreshCarsNumber(cars);
    return board;
}

function drawBackground(){
    var c = document.getElementById("board_canvas");
    var ctx = c.getContext("2d");
    ctx.beginPath();
    
    ctx.fillStyle = "gray";
    ctx.fillRect(0, 0, 500, 500);
    
    ctx.drawImage(traffic_lights_img, 500, 0);
    ctx.fillStyle = "black";
    ctx.fillRect(500, 0, 1, 500);
    ctx.stroke(); 
}

function drawBoard(rows, cols, board){    
    var cell_size = 500/cols;

    var c = document.getElementById("board_canvas");
    var ctx = c.getContext("2d");
    ctx.beginPath();

    for(var i = 0; i < rows; i++){
        for(var j = 0; j < cols; j++){
            //poziom
            if(i<rows/2){
                if(board[i][j].is_occupied==true) ctx.fillStyle = "blue";  
                else ctx.fillStyle = "white";   
                ctx.fillRect(j*cell_size, (i+(1+i)*10)*cell_size, cell_size, cell_size);
            }
            //pion
            else{
                if(board[i][j].is_occupied==true) ctx.fillStyle = "blue";
                else ctx.fillStyle = "white";  
                ctx.fillRect(((i-rows/2)+(1+(i-rows/2))*10)*cell_size, j*cell_size, cell_size, cell_size);
            }
        }
    }
    
    for(var i = 0; i < rows/2; i++){
        for(var j = 0; j < cols; j++){
            if((j==10 || j==21 || j==32 || j==43 || j==54)){
                if(board[i][j].is_occupied==true){
                    ctx.fillStyle = "blue";
                    ctx.fillRect(j*cell_size, (i+(1+i)*10)*cell_size, cell_size, cell_size);
                }
                if(board[i*2][j].is_occupied==true){
                    ctx.fillStyle = "blue";
                    ctx.fillRect(((i-rows/2)+(1+(i-rows/2))*10)*cell_size, j*cell_size, cell_size, cell_size);      
                }
            } 
        }
    }
    ctx.stroke();
}

function drawTrafficLights(state1, state2){
    var c = document.getElementById("board_canvas");
    var ctx = c.getContext("2d");

    //vertical
    ctx.beginPath();
    ctx.arc(550, 72.5, 17.5, 0, 2 * Math.PI, false);
    if(state1==2) ctx.fillStyle = 'green';
    else ctx.fillStyle = 'black'; 
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#006600';
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(550, 112.5, 17.5, 0, 2 * Math.PI, false);
    if(state1==1) ctx.fillStyle = 'orange';
    else ctx.fillStyle = 'black'; 
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#943100';
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(550, 152.5, 17.5, 0, 2 * Math.PI, false);
    if(state1==0) ctx.fillStyle = 'red';
    else ctx.fillStyle = 'black'; 
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#8f0101';
    ctx.stroke();

    //horizontal
    ctx.beginPath();
    ctx.arc(550, 347.5, 17.5, 0, 2 * Math.PI, false);
    if(state2==2) ctx.fillStyle = 'green';
    else ctx.fillStyle = 'black'; 
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#006600';
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(550, 387.5, 17.5, 0, 2 * Math.PI, false);
    if(state2==1) ctx.fillStyle = 'orange';
    else ctx.fillStyle = 'black'; 
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#943100';
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(550, 427.5, 17.5, 0, 2 * Math.PI, false);
    if(state2==0) ctx.fillStyle = 'red';
    else ctx.fillStyle = 'black';     
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#8f0101';
    ctx.stroke();
}

function changeTrafficLights(){
    if( typeof changeTrafficLights.counter == 'undefined' ) {
        changeTrafficLights.counter = 0;
        steps_till_traffic_light_change = 0;
    }
    changeTrafficLights.counter++;
    steps_till_traffic_light_change--;
    if(changeTrafficLights.counter<=5) traffic_lights=0; //zielone w poziomie
    else traffic_lights=1; //zielone w pionie

    //pomaranczowe
    if(changeTrafficLights.counter==1 || changeTrafficLights.counter==6){
        drawTrafficLights(1, 1);
        steps_till_traffic_light_change=5;
    }
    else if(changeTrafficLights.counter<=5) drawTrafficLights(2, 0);
    else drawTrafficLights(0, 2);

    if(changeTrafficLights.counter==10) changeTrafficLights.counter=0;
}

//LOGIKA AUTOMATU
function simulation(){
    var rows = parseInt(streets_number)*2;
    var cols = (rows/2+1)*10+rows/2;;

    drawBoard(rows, cols, board);
    drawChart(rows, cols, board);

    RefreshSlowDownPercent();
    RefreshMaxVelocity();

    var tmp_board = new Array(rows*2);
    for(var i = 0; i < rows*2; i++){
        tmp_board[i] = new Array(cols);
        for(var j = 0; j < cols; j++){
            tmp_board[i][j] = new Cell(false);
        }
    }

    var steps_till_traffic_light_change = steps_till_traffic_light_change*(simulation_speed/traffic_light_speed_step);

    for(var i = 0; i < rows; i++){
        for(var j = 0; j < cols; j++){
            //poziom i pion
            if(board[i][j].is_occupied==true){
                //losowe zwalnianie
                if(board[i][j].v>0 && Math.random()*100<=slow_down_percent){
                    board[i][j].v--;
                }
                else if(board[i][j].v<v_max) board[i][j].v++;
                var free_cells_ahead = 0;

                for(var k=1; k<=board[i][j].v; k++){
                    if(board[i][(j+k)%cols].is_occupied==false){ 
                        //1 to zielone w pionie
                        if(j+k%cols==10 || j+k%cols==21 || j+k%cols==32 || j+k%cols==43 || j+k%cols==54){
                            if(j!=cols-1){
                                if(i<rows/2 && traffic_lights==0) break;
                                else if(i>=rows/2 && traffic_lights==1) break;

                            }
                        }
                    }
                    else break;        
                    free_cells_ahead++;      
                }
                if(free_cells_ahead<=board[i][j].v) board[i][j].v = free_cells_ahead;
                tmp_board[i][(j+free_cells_ahead)%cols] = board[i][j];
            
            }
        }
    }

    for(var i = 0; i < rows; i++){
        for(var j = 0; j < cols; j++){
            board[i][j] = tmp_board[i][j];
        }
    }

}

function startSimulation(){
    initializeSimulation();
    var new_speed = document.getElementById("simulation_speed").value;
    simulation_speed = parseInt(new_speed);
    var new_traffic_light_speed = document.getElementById("traffic_light_speed").value;
    traffic_light_speed_step = parseInt(new_traffic_light_speed)/10;
    id_simulation = setInterval(function(){ simulation(); }, simulation_speed);
    id_traffic_lights = setInterval(function(){ changeTrafficLights(); }, traffic_light_speed_step);
}

function stopSimulation(){
    average_velocity_data = [];
    if(id_simulation!=0){
        clearInterval(id_simulation);
        average_velocity_data = [];
        drawAverageVelocityChart();
    }
    if(id_traffic_lights!=0){
        clearInterval(id_traffic_lights);
    }
}

function updateSpeed(){
    clearInterval(id_simulation);
    var new_speed = document.getElementById("simulation_speed").value;
    simulation_speed = parseInt(new_speed);
    id_simulation = setInterval(function(){ simulation(); }, simulation_speed);
}

function updateTrafficLightSpeed(){
    if(id_traffic_lights!=0){
        clearInterval(id_traffic_lights);
        var new_traffic_light_speed = document.getElementById("traffic_light_speed").value;
        traffic_light_speed_step = parseInt(new_traffic_light_speed)/10;
        id_traffic_lights = setInterval(function(){ changeTrafficLights(); }, traffic_light_speed_step);
    }
}

function drawChart(rows, cols, board){
    var average_velocity = 0;
    for(var i = 0; i < rows; i++){
        for(var j = 0; j < cols; j++){
            if(board[i][j].is_occupied==true){
                average_velocity += board[i][j].v;
            }
        }
    }
    average_velocity /= how_many_cars;
    average_velocity_data.push(average_velocity);
    RefreshAverageVelocity(average_velocity);
    drawAverageVelocityChart();
}

function drawAverageVelocityChart(){
    // google.charts.load('current', {'packages':['corechart']});
    // google.charts.setOnLoadCallback(drawChart);
    
    // function drawChart(){
    //     var data = new google.visualization.DataTable();
    //     data.addColumn("number", "Czas");
    //     data.addColumn("number", "Average velocity");

    //     for(var i=0; i<average_velocity_data.length; i++){
    //         data.addRow([i, average_velocity_data[i]]);
    //     }
    //     var options = {
    //     curveType: 'function',
    //     hAxis: {title: "Time"},
    //     vAxis: {title: "Average velocity [cells/step]"}
    //     };
    //     var chart = new google.visualization.LineChart(document.getElementById("living_percent_chart"));
    //     chart.draw(data, options);
    // }
    
}


function RefreshOccupiedPercent(){
    var input = document.getElementById("occupied_percent_beginning").value;
    occupied_percent_beginning = parseFloat(input);
}

function RefreshSlowDownPercent(){
    var input = document.getElementById("slow_down_probability").value;
    slow_down_percent = parseFloat(input);
}

function RefreshMaxVelocity(){
    var input = document.getElementById("max_velocity").value;
    v_max = parseInt(input);
}

function RefreshAverageVelocity(average_speed){
    document.getElementById("average_speed").innerHTML = average_speed+" cells/step";
}

function RefreshCarsNumber(how_many_cars){
    document.getElementById("how_many_cars").innerHTML = how_many_cars;
}


