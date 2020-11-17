package controllers;

import java.io.IOException;
import java.util.HashMap;

import application.App;
import application.Main;
import javafx.animation.AnimationTimer;
import javafx.event.Event;
import javafx.scene.Node;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.effect.DropShadow;
import javafx.scene.effect.GaussianBlur;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.Pane;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import view.MapView;

public class SoundController extends AnimationTimer {

    float vol;

    @Override
    public void handle(long now) {


        //frequently get the amplitude
        vol = model.SoundModel.getVolume();
        System.out.println(vol);

        //sound range: 0.01-0.6

        //initial view

        if(application.Main.root.lookup("#level-view").isVisible()) {
            //shout to start
            System.out.println(application.Main.root.lookup("level-view"));
            if(vol > 0.03) {
                System.out.print("Voice Detected: Shout to Start");
                //Button btn = view.SelectCharacterView.btnnext;
                view.SelectCharacterView.btnnext.setDisable(false);
//                view.SelectCharacterView.btnnext.setStyle("-fx-background-color: #FFA23D;");


                //view.SelectLevelView.shout.setEffect(new GaussianBlur());

                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }

                //switch scene
                //TODO Please help to implement mapView
                App app = null;
                try {
                    app = new App(0);
                    Pane mapView = new Pane();
                    mapView.getChildren().add(app);
                    application.Main.root.getChildren().add(mapView);
//                    System.out.println("soundController charNum:"+app.characterNum);
                    app.mapView.pig.init();
                    this.stop();
                } catch (IOException e) {
                    e.printStackTrace();
                }

            }
        }

    }

    @Override
    public void stop() {

        super.stop();

    }



}
