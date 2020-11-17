package view;

import javafx.scene.layout.FlowPane;


import javafx.geometry.Insets;
import javafx.scene.Node;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.FlowPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.scene.text.Text;

public class SelectLevelView extends FlowPane {

    public Text LevTitle;
    public Button btnnext;
    public Button lev1= new Button("Beginner");;
    public Button lev2= new Button("Intermediate");;
    public Button lev3= new Button("Expert");;
    public static Label shout;
    public Button previous;


    VBox paneTitle = new VBox();
    VBox paneLevel = new VBox(20);
    VBox paneShout = new VBox();
    HBox paneControl = new HBox(300);

    public SelectLevelView() {
        //previous = new Button();
        //btnnext = new Button();

        shout = new Label("SHOUT TO START");

        lev1.setPrefSize(300,40);
        lev2.setPrefSize(300,40);
        lev3.setPrefSize(300,40);
        shout.setPrefSize(200,40);


        lev1.setFont(Font.font("Arial", 15));
        lev1.setStyle("-fx-background-color: transparent; ");
        lev1.setTextFill(Color.WHITE);
        lev2.setFont(Font.font("Arial", 15));
        lev2.setStyle("-fx-background-color: transparent; ");
        lev2.setTextFill(Color.WHITE);
        lev3.setFont(Font.font("Arial", 15));
        lev3.setStyle("-fx-background-color: transparent; ");
        lev3.setTextFill(Color.WHITE);
        shout.setFont(Font.font("Arial", FontWeight.BOLD, 15));
        shout.setStyle("-fx-background-color:transparent ; ");
        shout.setTextFill(Color.WHITE);

        LevTitle = new Text ("SELECT YOUR LEVEL");
        LevTitle.setFont(Font.font("Arial", FontWeight.BOLD, 30));
        LevTitle.setFill(Color.WHITE);



        btnnext = new Button("Next");
        btnnext.setDisable(true);
        btnnext.setFont(Font.font("Arial", FontWeight.BOLD, 15));
        //btnnext.setStyle("-fx-background-color: darkgrey; ");
        btnnext.setTextFill(Color.WHITE);
        btnnext.setPrefWidth(150);
        btnnext.setId("btn-next");

        previous = new Button("Previous");
        previous.setFont(Font.font("Arial", FontWeight.BOLD, 15));
        previous.setStyle("-fx-background-color: #FFA23D; ");
        previous.setTextFill(Color.WHITE);
        previous.setPrefWidth(150);
        previous.setId("btn-prev");


        paneTitle.getChildren().add(LevTitle);
        paneTitle.setPadding(new Insets(100,50,50,250));
        paneLevel.getChildren().addAll(lev1,lev2,lev3,shout);
        paneLevel.setPadding(new Insets(50,50,50,250));
        //paneLevel.setAlignment(Pos.CENTER);
        paneShout.getChildren().add(shout);
        paneShout.setPadding(new Insets(150,50,50,300));
        paneControl.getChildren().addAll(previous,btnnext);
//        paneControl.getChildren().addAll(previous);
        paneControl.setPadding(new Insets(0,100,0,100));

        this.getChildren().addAll(paneTitle,paneLevel,paneShout,paneControl);
        this.setStyle("-fx-background-color: #00426C");
        this.setId("level-view");

    }
}

