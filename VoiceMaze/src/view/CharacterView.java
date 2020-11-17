package view;

import application.Main;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.StackPane;
import model.CharModel;
import model.MapModel;

import java.io.IOException;

public class CharacterView extends StackPane {

    public int rowNum, colNum;
    public MapModel mapModel;
    private ImageView character;
    public MapView mapView;
    public CharModel myCharModel;
    public int charNum;




    public CharacterView() {
        myCharModel = new CharModel();
        charNum=  myCharModel.getCharNum();
        character = DrawCharacter(charNum);
        this.getChildren().addAll(character);
    }
    public void init(){
        character = DrawCharacter(charNum);
        this.getChildren().addAll(character);
    }
    public void repaint(){

        System.out.println("repaint is called");
        this.getChildren().clear();
        character = DrawCharacter(charNum);
        this.getChildren().addAll(character);

    }

//    public void moveForward() throws IOException {
//        mapModel = new MapModel();
////        int[][] map = mapModel.readMap("0.txt");
//        if(
////                x < 20 && map[x+1][y] == 0
//                x >=0 && y>=0
//        ){
//            //x,y 初始坐标有问题
////            this.setTranslateX(x*40+20);
//            this.x= x * 40+20;
//            repaint(0);
//
////            this.setTranslateX(xValue);
//            System.out.println("afterX"+x);
//            x++;
//        }
//    }


    public ImageView DrawCharacter( int characterNum ){
        // to-do integrate characterNum to string
        String filePath = "img/G"+characterNum+".png";
        System.out.println("charView: filepath"+filePath);
        Image characterImg = new Image("img/G"+characterNum+".png");
        ImageView imgView = new ImageView();
        imgView.setImage(characterImg);
        imgView.setFitHeight(40);
        imgView.setFitWidth(40);

        return imgView;
    }

//    public void jump(){
//        mapModel = new MapModel();
//        if(y > 0 && mapModel.map[x][y-1] == 1){
//            this.setTranslateY(this.y * 40 - 25);
//            y--;
//        }
//
//    }

}
