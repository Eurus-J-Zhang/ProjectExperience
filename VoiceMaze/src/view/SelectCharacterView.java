package view;

import javafx.geometry.Insets;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.scene.control.ToggleButton;
import javafx.scene.control.ToggleGroup;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.FlowPane;
import javafx.scene.layout.HBox;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.scene.text.Text;

public class SelectCharacterView extends FlowPane{

    public static Button btnnext;
    public Text CharTitle;
    public ToggleGroup charGroup = new ToggleGroup();
    public ToggleButton char1= new ToggleButton();
    public ToggleButton char2= new ToggleButton();
    public ToggleButton char3= new ToggleButton();
    //public Button submit= new Button("SUBMIT");
    public TextField textname;

    HBox paneTitle = new HBox();
    HBox paneChar = new HBox(70);
    HBox paneEnter = new HBox(70);
    HBox paneNext = new HBox();

    public SelectCharacterView() {

        CharTitle = new Text ("SELECT YOUR CHARACTER");
        CharTitle.setFont(Font.font("Arial", FontWeight.BOLD, 30));
        CharTitle.setFill(Color.WHITE);

        char1.setPrefSize(150,150);
        char1.setStyle("-fx-background-color: transparent; ");
        char2.setPrefSize(150,150);
        char2.setStyle("-fx-background-color: #00426C; ");
        char3.setPrefSize(150,150);
        char3.setStyle("-fx-background-color: #00426C; ");

        Image imgpig1 = new Image("img/G0.png");
        ImageView viewpig1 = new ImageView(imgpig1);
        viewpig1.setFitHeight(100);
        viewpig1.setPreserveRatio(true);
        char1.setGraphic(viewpig1);

        Image imgpig2 = new Image("img/G1.png");
        ImageView viewpig2 = new ImageView(imgpig2);
        viewpig2.setFitHeight(100);
        viewpig2.setPreserveRatio(true);
        char2.setGraphic(viewpig2);

        Image imgpig3 = new Image("img/G2.png");
        ImageView viewpig3 = new ImageView(imgpig3);
        viewpig3.setFitHeight(100);
        viewpig3.setPreserveRatio(true);
        char3.setGraphic(viewpig3);

        /*

        submit.setFont(Font.font("Arial", FontWeight.BOLD, 15));
        submit.setStyle("-fx-background-color: #FFA23D; ");
        submit.setTextFill(Color.WHITE);
        submit.setPrefWidth(100);


         */

        textname = new TextField("Enter your character name here and press 'ENTER'");
        textname.setPrefWidth(400);

        btnnext = new Button("Next");
        btnnext.setFont(Font.font("Arial", FontWeight.BOLD, 15));
        btnnext.setStyle("-fx-background-color: #FFA23D; ");
        btnnext.setTextFill(Color.WHITE);
        btnnext.setPrefWidth(100);
        btnnext.setId("btn-next");

        paneTitle.getChildren().add(CharTitle);
        paneChar.getChildren().addAll(char1,char2,char3);
        //paneEnter.getChildren().addAll(textname,submit);
        paneEnter.getChildren().addAll(textname);
        paneNext.getChildren().add(btnnext);

        paneTitle.setPadding(new Insets(100,50,50,200));
        paneChar.setPadding(new Insets(50,50,50,100));
        paneEnter.setPadding(new Insets(50,50,50,100));
        paneNext.setPadding(new Insets(50,50,50,570));




        this.getChildren().add(paneTitle);
        this.getChildren().add(paneChar);
        this.getChildren().add(paneEnter);
        this.getChildren().add(paneNext);
        this.setStyle("-fx-background-color: #00426C");
        this.setId("select-char-view");
    }
}

