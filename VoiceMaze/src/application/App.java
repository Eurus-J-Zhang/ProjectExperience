package application;

//import controllers.CharController;
import javafx.animation.AnimationTimer;
import javafx.scene.control.Button;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.Pane;
import model.SoundModel;
import view.MapView;

import java.io.IOException;

public class App extends AnchorPane {
    public MapView mapView;
    public Button exitBtn;
    public SoundModel soundModel;
    public int mapNum;
    public int characterNum;

    public App(int mapNum) throws IOException {
        initiate();
        setVisible(true);
        //Add CharController
        CharController myCharController = new CharController();
        myCharController.start();
    }

    public void initiate() throws IOException {
        mapView = new MapView();
        exitBtn = mapView.exitBtn;
        this.getChildren().add(mapView);
    }

    public class CharController extends AnimationTimer {
        public SoundModel mySoundModel;
        public float vol;

        @Override
        public void handle(long now) {
            vol = mySoundModel.getVolume();

            double pigX = mapView.pig.getLayoutX();
            double pigY = mapView.pig.getLayoutY();
            int[][] map = mapView.map;
            int x = mapView.pig.colNum;
            int y = mapView.pig.rowNum;

//            if(vol>=0){
//                // if box below is 0, then give a stable drop speed
//                System.out.println("vol>0 is detected");
//                System.out.println("y:"+y);
//                System.out.println("x:"+x);
//                System.out.println("boxbelow:"+map[y+1][x]);
//
//                if(vol > 0.02){
//                    //if right box is 0, give a stable right speed
//                    System.out.println("vol >0.2 is detected");
//                    if(map[y][x+1]==0){
//                        System.out.println("right speed is added");
//                        pigX=pigX+40;
//                        mapView.pig.setLayoutX(pigX);
//                        mapView.pig.colNum=x+1;
//                        try {
//                            Thread.sleep(50);
//                        } catch (InterruptedException e) {
//                            e.printStackTrace();
//                        }
//                    }else {
//                        System.out.println("right speed is not added");
//                    }
//                    if(vol >0.05){
//                        //if box above is 0, give a stable up speed
//                        System.out.println("vol > 0.05 is detected");
//                        if(map[y-1][x]==0){
//                            System.out.println("up speed is added");
//                            pigY=pigY-80;
//                            mapView.pig.setLayoutY(pigY);
//                            mapView.pig.rowNum = y-1;
//                            try {
//                                Thread.sleep(50);
//                            } catch (InterruptedException e) {
//                                e.printStackTrace();
//                            }
//                        }else{
//                            // else, then stop
//                            System.out.println("up speed is not added");
//                        }
//
//                    }
//                }
//
//                //drop speed
////                if(map[y+1][x]==0){
////                    System.out.println("drop speed is called");
////                    pigY= pigY+40;
////                    mapView.pig.setLayoutY(pigY);
////                    mapView.pig.rowNum = y + 1;
////                    try {
////                        Thread.sleep(50);
////                    } catch (InterruptedException e) {
////                        e.printStackTrace();
////                    }
////                }else{
////                    System.out.println("drop speed is not added");
////                }
//            }

            if(vol > 0.02 && vol < 0.05 ){
                System.out.println("right is called");
                if(map[y][x+1]==0){
                    pigX=pigX+40;
                    mapView.pig.setLayoutX(pigX);
                    mapView.pig.colNum=x+1;
                    System.out.println("colNum"+mapView.pig.colNum);
                    try {
                        Thread.sleep(50);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }
                //if right box is 0, give a stable right speed

            }
            if(vol >= 0.05 ){
                if(map[y-1][x]==0){
                    pigY=pigY-40;
                    System.out.println("up is called");
                    mapView.pig.setLayoutY(pigY);
                    mapView.pig.rowNum = y-1;
                    try {
                        Thread.sleep(50);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }
                //if box above is 0, give a stable up speed

//                else if(map[y-1][x]==1){
//                    // else, then stop
//                    pigY=pigY+0;
//                    mapView.pig.setLayoutY(pigY);
//                    mapView.pig.rowNum =y;
//                    System.out.println("up speed is not added");
//                }

            }
            
            //System.out.println("final y:"+y);
            //System.out.println("final x"+x);
            //if(y==1 && x==15){
            //    System.out.println("Success!!!!!");
           //     //TODO add a success popup
           // }
//
//            if(y==7 && x==13){
//                System.out.println("Fail!!!!!");
//                //TODO add a game over popup
//            }

//            if(vol >= 0){
//                System.out.println("y:"+y);
//                System.out.print("x:"+x);
//                if(pigX >= 0 && pigX <= 800 && map[y+1][x] == 0) {
//                    System.out.println("gravity is called");
//                    pigY = pigY + 40;
//                    mapView.pig.setLayoutY(pigY);
//                    mapView.pig.rowNum = y + 1;
//                    try {
//                        Thread.sleep(50);
//                    } catch (InterruptedException e) {
//                        e.printStackTrace();
//                    }
//                }else
//                if(pigY<=0 && pigY>=-800 && map[y+1][x]==1){
//
//                    System.out.println("hit the ground");
//                    mapView.pig.setLayoutY(pigY);
//                    mapView.pig.rowNum=y;
//                    try {
//                        Thread.sleep(50);
//                    } catch (InterruptedException e) {
//                        e.printStackTrace();
//                    }
//
//                }
//                if (vol > 0.02) {
////                System.out.println("moveForward map[][]"+map[y][x+1]);
//                    if (pigX >= 0 && pigX <= 800 && map[y][x + 1] == 0) {
//                        System.out.println("x:" + x + "y:" + y);
//
//                        System.out.println("moveforward is called");
//                        pigX = pigX + 40;
//                        mapView.pig.setLayoutX(pigX);
//                        mapView.pig.colNum = x + 1;
//                        System.out.println("xPointafter:" + mapView.pig.colNum);
//                        try {
//                            Thread.sleep(50);
//                        } catch (InterruptedException e) {
//                            e.printStackTrace();
//                        }
//                    }
//                    if (vol > 0.05) {
//                        System.out.println("jump map[][]" + map[y - 1][x]);
//                        System.out.println("pigY:" + pigY);
//                        if (pigY <= 0 && pigY >= -800 && y > 0 && map[y - 1][x] == 0) {
//                            System.out.println("jump is called");
//                            pigY = pigY - 80;
//                            mapView.pig.setLayoutY(pigY);
//                            mapView.pig.rowNum = y - 1;
//                            try {
//                                Thread.sleep(50);
//                            } catch (InterruptedException e) {
//                                e.printStackTrace();
//                            }
//                        }
//                    }
//                }
//            }




        }
        @Override
        public void stop() {

            super.stop();

        }
    }

}
