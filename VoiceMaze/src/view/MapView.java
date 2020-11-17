package view;


//import controllers.CharController;
import javafx.animation.KeyFrame;
import javafx.animation.KeyValue;
import javafx.animation.Timeline;
import javafx.application.Platform;
import javafx.beans.property.IntegerProperty;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.geometry.Insets;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.util.Duration;
import model.CharModel;
import model.MapModel;
import model.MapNumModel;


import java.io.IOException;

public class MapView extends FlowPane {
    public static int boxSize=40;
    public int[][] map = null;
    public Button exitBtn;
    public Button startBtn;
    //public Button backBtn;
    public AnchorPane mazeView;
    public Label timer;
    public Label timertext;
    public CharacterView pig;
    public MapModel newMap;
    public static final Integer STARTTIME = 100;
    public Timeline timeline;
    public String mapfile;

    public IntegerProperty timeSeconds;



    HBox paneTitle = new HBox(80);

    public MapView() throws IOException {
        timeSeconds= new SimpleIntegerProperty(STARTTIME);

        newMap = new MapModel();
        // to-do :  change the mapName based on level selection

        pig = new CharacterView();
        //mapv = new MapView()

        //root = new BorderPane();

        /*
        backBtn = new Button("Back");
        backBtn.setPrefWidth(100);
        backBtn.setStyle("-fx-background-color:ORANGE");
        backBtn.setTextFill(Color.WHITE);

         */

        startBtn = new Button("Start the game");
        //startBtn.setPrefSize(200,50);
        startBtn.setStyle("-fx-background-color:ORANGE");
        startBtn.setTextFill(Color.WHITE);


        startBtn.setOnMouseClicked(e-> {

            if (timeline != null) {
                timeline.stop();
            }
            timeSeconds.set(view.MapView.STARTTIME);
            timeline = new Timeline();
            timeline.getKeyFrames().add(
                    new KeyFrame(Duration.seconds(101),
                            new KeyValue(timeSeconds, 0)));
            timeline.playFromStart();
        });


        exitBtn = new Button("Exit Game");
        exitBtn.setStyle("-fx-background-color:ORANGE");
        exitBtn.setTextFill(Color.WHITE);
        exitBtn.setOnMouseClicked(e -> Platform.exit());


        timer = new Label("Time Left:");
        timer.setTextFill(Color.WHITE);
        timertext = new Label();
        timertext.setTextFill(Color.WHITE);
        timertext.textProperty().bind(timeSeconds.asString());

        paneTitle.setPadding(new Insets(10,10,10,50));
        paneTitle.getChildren().addAll(startBtn,timer, timertext,exitBtn);

        mazeView = new AnchorPane();
        MapNumModel myMapNumModel = new MapNumModel();

        mapfile = "src/"+myMapNumModel.getMapNum()+".txt";
        //read the map from txt file
        map = newMap.readMap(mapfile);


        for (int i = 0; i < map.length; i++) {
            for (int j = 0; j < map[0].length; j++) {
                Box box = new Box(j,i);
                mazeView.getChildren().addAll(box);


                if(i==14 && j==0){
                    pig.setTranslateX(j);
                    pig.setTranslateY((i-1)*boxSize);
                    pig.rowNum=i-1;
                    pig.colNum=j;
                    mazeView.getChildren().addAll(pig);//box,
                }
                else if(map[i][j]==1){

                    Obstacle wall = new Obstacle(j,i);
                    mazeView.getChildren().addAll(wall);

                }else if(map[i][j]==3){
                    Flag flag = new Flag(j,i);
                    mazeView.getChildren().addAll(flag);
                }else if(map[i][j]==2){
                    Boom boom = new Boom(j,i);
                    mazeView.getChildren().addAll(boom);

                }
            }
        }


        this.getChildren().add(paneTitle);
        this.getChildren().add(mazeView);


    }

    public class Box extends StackPane {
        Rectangle box = new Rectangle(boxSize,boxSize);
        public Box(int x, int y) {
            box.setFill(Color.rgb(255,184,84));//255,184,84
            getChildren().addAll(box);
            this.setTranslateX(x * boxSize);
            this.setTranslateY(y * boxSize);
        }
    }

    public class Obstacle extends StackPane{
        Rectangle obstacle = new Rectangle(boxSize,boxSize);
        public Obstacle(int x, int y) {
            obstacle.setFill(Color.rgb(1,82,133));
            getChildren().addAll(obstacle);
            this.setTranslateX(x * boxSize);
            this.setTranslateY(y * boxSize);
        }
    }

    public class Flag extends StackPane{
        Image flag = new Image("img/Flag.png");
        ImageView flagView= new ImageView();
        public Flag(int x, int y){
            flagView.setImage(flag);
            flagView.setFitHeight(boxSize);
            flagView.setFitWidth(boxSize);
            getChildren().addAll(flagView);
            this.setTranslateX(x * boxSize);
            this.setTranslateY(y * boxSize);


        }


    }

    public class Boom extends StackPane{
        Image boom = new Image("img/bomb.png");
        ImageView boomView= new ImageView();
        public Boom(int x, int y){
            boomView.setImage(boom);
            boomView.setFitHeight(boxSize);
            boomView.setFitWidth(boxSize);
            getChildren().addAll(boomView);
            this.setTranslateX(x * boxSize);
            this.setTranslateY(y * boxSize);


        }


    }
}

//Reference: http://yun.itheima.com/open/404.html

