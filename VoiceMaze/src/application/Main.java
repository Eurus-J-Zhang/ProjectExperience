package application;

import javafx.application.Application;
import javafx.event.EventHandler;
import javafx.scene.Scene;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.Pane;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;
import model.CharModel;
import model.MapNumModel;
import model.SoundModel;
import view.SelectCharacterView;
import view.SelectLevelView;

import java.io.IOException;

import controllers.SoundController;
import view.WelcomeView;

public class Main extends Application {

    public static StackPane root;

    public int mapNum;
    private Stage secondaryStage;

    public static void main(String[] args) {
        controllers.CaptureSoundController.main(args);
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) throws Exception{

        SoundController timer = new SoundController();

        root = new StackPane();
        root.setPrefSize(800, 1600);
        Scene scene = new Scene(root);
        WelcomeView wlv = new WelcomeView();
        Scene WelScene = new Scene(wlv, 300,200);
        secondaryStage = new Stage();
        secondaryStage.setTitle("Welcome");
        secondaryStage.setScene(WelScene);
        secondaryStage.hide();


//        System.out.println("main:"+this.characterNum);
//        CharModel myCharModel= new CharModel();
//        int charNum = myCharModel.getCharNum();

        App app = new App(this.mapNum);
        Pane mapView = new Pane();
        mapView.getChildren().add(app);


        SelectCharacterView scv= new SelectCharacterView();
        SelectLevelView slv= new SelectLevelView();


        scv.setOnKeyPressed(new EventHandler<KeyEvent>()
        {
            @Override
            public void handle(KeyEvent ke)
            {
                if (ke.getCode().equals(KeyCode.ENTER))
                {
                    secondaryStage.show();
                }
            }
        });


        scv.btnnext.setOnMouseClicked( e-> {
            root.getChildren().add(slv);
            timer.start();
//            System.out.println("volume From SoundModel"+SoundModel.getVolume());
        });
        slv.btnnext.setOnMouseClicked( e-> {
            System.out.println("btn is clicked");
            root.getChildren().clear();
            root.getChildren().add(mapView);
        });
        slv.previous.setOnMouseClicked(e-> {
            root.getChildren().clear();
            root.getChildren().add(scv);
            timer.stop();
        });

        /*
        app.exitBtn.setOnMouseClicked(e -> {
            root.getChildren().add(slv);
        });

         */
        CharModel myCharModel = new CharModel();


        scv.char1.setOnMouseClicked( e -> {
            scv.char1.setStyle("-fx-background-color: #FFA23D; ");
            scv.char2.setStyle("-fx-background-color: transparent; ");
            scv.char3.setStyle("-fx-background-color: transparent; ");
            myCharModel.setCharNum(0);
            app.mapView.pig.repaint();
        });

        scv.char2.setOnMouseClicked( e -> {
            scv.char2.setStyle("-fx-background-color: #FFA23D; ");
            scv.char1.setStyle("-fx-background-color: transparent; ");
            scv.char3.setStyle("-fx-background-color: transparent; ");
            myCharModel.setCharNum(1);
            app.mapView.pig.repaint();
        });

        scv.char3.setOnMouseClicked( e -> {
            scv.char3.setStyle("-fx-background-color: #FFA23D; ");
            scv.char1.setStyle("-fx-background-color: transparent; ");
            scv.char2.setStyle("-fx-background-color: transparent; ");
            myCharModel.setCharNum(2);
            app.mapView.pig.repaint();
        });

        MapNumModel myMapNumModel = new MapNumModel();

        slv.lev1.setOnMouseClicked( e -> {
            slv.lev1.setStyle("-fx-background-color: #FFA23D; ");
            slv.lev2.setStyle("-fx-background-color: transparent; ");
            slv.lev3.setStyle("-fx-background-color: transparent; ");
            myMapNumModel.setMapNum(0);
            try {
                app.initiate();
            } catch (IOException ioException) {
                ioException.printStackTrace();
            }
        });

        slv.lev2.setOnMouseClicked( e -> {
            slv.lev2.setStyle("-fx-background-color: #FFA23D; ");
            slv.lev1.setStyle("-fx-background-color: transparent; ");
            slv.lev3.setStyle("-fx-background-color: transparent; ");
            myMapNumModel.setMapNum(1);
            try {
                app.initiate();
            } catch (IOException ioException) {
                ioException.printStackTrace();
            }

        });

        slv.lev3.setOnMouseClicked( e -> {
            slv.lev3.setStyle("-fx-background-color: #FFA23D; ");
            slv.lev1.setStyle("-fx-background-color: transparent; ");
            slv.lev2.setStyle("-fx-background-color: transparent; ");
            myMapNumModel.setMapNum(2);
            try {
                app.initiate();
            } catch (IOException ioException) {
                ioException.printStackTrace();
            }
        });

        root.getChildren().add(scv);
        root.setPrefSize(800, 800);
        primaryStage.setTitle("VoiceControlMario");
        primaryStage.setScene(scene);
        primaryStage.show();

    }
}
