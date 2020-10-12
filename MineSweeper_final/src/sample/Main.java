package sample;

import javafx.animation.KeyFrame;
import javafx.animation.KeyValue;
import javafx.animation.Timeline;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.beans.property.IntegerProperty;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Group;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.TextField;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.input.*;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.stage.Stage;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.text.Text;
import javafx.util.Duration;



import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;


public class Main extends Application
{

    public final Text target = new Text("Dragging Area");
    private ImageView imageView;
    private Button buttonClose;
    private Button smilingface;
    private Label mineleft;
    private Label minelefttext;
    private Label timespent;
    private Label timespenttext;
    private Label dropping;
    //private Text comment;
    private Text tutorial;
    private Text welcome;

    private TextField textname;
    private Stage secondaryStage;
    private EventHandler<KeyEvent> textnameListener;
    private EventHandler<ActionEvent> buttonCloseListener;
    private static final Integer STARTTIME = 100;
    private Timeline timeline;
    // Make timeSeconds a Property
    private IntegerProperty timeSeconds = new SimpleIntegerProperty(STARTTIME);


    private static final int TILE_SIZE = 30;
    private static final int W = 300;
    private static final int H = 300;

    private static final int X_TILES = W / TILE_SIZE;
    private static final int Y_TILES = H / TILE_SIZE;

    private Tile[][] grid = new Tile[X_TILES][Y_TILES];
    private Scene scene;

    private Parent createContent() {
        Pane root = new Pane();
        root.setPrefSize(W, H);

        for (int y = 0; y < Y_TILES; y++) {
            for (int x = 0; x < X_TILES; x++) {
                Tile tile = new Tile(x, y, Math.random() <0.1);

                grid[x][y] = tile;
                root.getChildren().add(tile);
            }
        }

        for (int y = 0; y < Y_TILES; y++) {
            for (int x = 0; x < X_TILES; x++) {
                Tile tile = grid[x][y];

                if (tile.hasBomb)
                    continue;

                long bombs = getNeighbors(tile).stream().filter(t -> t.hasBomb).count();

                if (bombs > 0)
                    tile.text.setText(String.valueOf(bombs));
            }
        }

        return root;
    }

    private List<Tile> getNeighbors(Tile tile) {
        List<Tile> neighbors = new ArrayList<>();

        // ttt
        // tXt
        // ttt

        int[] points = new int[] {
                -1, -1,
                -1, 0,
                -1, 1,
                0, -1,
                0, 1,
                1, -1,
                1, 0,
                1, 1
        };

        for (int i = 0; i < points.length; i++) {
            int dx = points[i];
            int dy = points[++i];

            int newX = tile.x + dx;
            int newY = tile.y + dy;

            if (newX >= 0 && newX < X_TILES
                    && newY >= 0 && newY < Y_TILES) {
                neighbors.add(grid[newX][newY]);
            }
        }

        return neighbors;
    }

    private class Tile extends StackPane {
        private int x, y;
        private boolean hasBomb;
        private boolean isOpen = false;

        private Rectangle border = new Rectangle(TILE_SIZE - 2, TILE_SIZE - 2);
        private Text text = new Text();
        //public Label q = new Label("?");

        public Tile(int x, int y, boolean hasBomb) {
            this.x = x;
            this.y = y;
            this.hasBomb = hasBomb;

            border.setStroke(Color.LIGHTGRAY);

            text.setFont(Font.font(18));
            text.setText(hasBomb ? "X" : "");
            text.setVisible(false);
           // q.setVisible(false);

            text.setOnDragDetected(new EventHandler <MouseEvent>() {
                public void handle(MouseEvent event) {
                    /* drag was detected, start drag-and-drop gesture*/
                    System.out.println("onDragDetected");

                    /* allow any transfer mode */
                    Dragboard db = text.startDragAndDrop(TransferMode.ANY);

                    /* put a string on dragboard */
                    ClipboardContent content = new ClipboardContent();
                    content.putString(text.getText());
                    db.setContent(content);

                    event.consume();
                }
            });


            target.setFont(Font.font("Arial", FontWeight.BOLD, 15));

            target.setOnDragDropped(new EventHandler <DragEvent>() {
                public void handle(DragEvent event) {
                    /* data dropped */
                    System.out.println("onDragDropped");
                    /* if there is a string data on dragboard, read it and use it */
                    Dragboard db = event.getDragboard();
                    boolean success = false;
                    if (db.hasString()) {

                        if (db.getString().equals("X")){
                            target.setText("Yes");
                        }
                        else{
                            target.setText("No");
                        }

                        success = true;
                    }
                    /* let the source know whether the string was successfully
                     * transferred and used */
                    event.setDropCompleted(success);

                    event.consume();
                }
            });

            getChildren().addAll(border, text);

            setTranslateX(x * TILE_SIZE);
            setTranslateY(y * TILE_SIZE);


            setOnMouseClicked(e -> {
                if (e.getButton() == MouseButton.PRIMARY) {
                    open();
                }
                if (e.getButton() == MouseButton.SECONDARY) {
                    if (border.getFill() == Color.RED) {
                        question();
                    } else {
                        mark();
                    }
                } }); }



        public void question(){

            border.setFill(Color.GREEN);
          //  q.setVisible(false);
            text.setVisible(true);
            text.setFill(Color.GREEN);
        }

        public void mark(){
            if (isOpen)
                return;
            border.setFill(Color.RED);
           // q.setVisible(false);
            text.setVisible(false);
        }

        public void open() {
            if (isOpen)
                return;

            if (hasBomb) {
                System.out.println("Game Over");
                //scene.setRoot(createContent());
                return;
            }

            isOpen = true;
            text.setVisible(true);
            text.setFill(Color.BLACK);
            border.setFill(null);
           // q.setVisible(false);

            if (text.getText().isEmpty()) {
                getNeighbors(this).forEach(Tile::open);
            }
        }
    }




    // main here …
    @Override
    public void start(Stage primaryStage) throws Exception
    {


        FlowPane root = new FlowPane();

        Scene scene = new Scene(root, 350, 680);

        initListener();
        initGUI(root);

        primaryStage.setTitle("MineSweeper");
        primaryStage.setScene(scene);
        primaryStage.show();

    }
    public void initListener()
    {
        buttonCloseListener = new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                Platform.exit();
            }
        };

        textnameListener=new EventHandler<KeyEvent>() {
            @Override
            public void handle(KeyEvent e) {

                if (e.getCode().equals(KeyCode.ENTER)) {
                    secondaryStage.show();
                }
            }
        };


    }
    public void initGUI(Pane root) throws FileNotFoundException
    {

        //paneF the first pane
        VBox paneF = new VBox();
        paneF.setPadding(new Insets(10,10,10,10));
        root.getChildren().add(paneF);

        textname = new TextField("Please type your name and press Enter on keyboard");
        textname.setPrefWidth(330);
        paneF.getChildren().add(textname);

        // A new scene when enter the name

        GridPane child = new GridPane();
        child.setPadding(new Insets(10, 10, 10, 10));
        child.setMinSize(100, 100);
        child.setVgap(5);
        child.setHgap(5);

        Label l = new Label("Hello, welcome to the Mine Sweeper!");
        child.add(l,0,4,4,1); // adding a control across multiple cells

        Scene scene_two = new Scene(child, 300,150 );
        // creating a stage/window to add the scene graph
        secondaryStage = new Stage();
        secondaryStage.setTitle("Welcome");
        secondaryStage.setScene(scene_two);
        secondaryStage.hide(); // secondary window hidden by default

        HBox paneButtons = new HBox();
        paneButtons.setPadding(new Insets(10, 10, 10, 10));
        paneButtons.setSpacing(10);
        paneButtons.setAlignment(Pos.CENTER_LEFT);

        welcome = new Text("Welcome");
        paneButtons.getChildren().add(welcome);
        textname.setOnKeyPressed(textnameListener);


        //paneA
        VBox paneA = new VBox();
        paneA.setPadding(new Insets(10,20,10,20));
        root.getChildren().add(paneA);

        mineleft = new Label("Mine in total:");
        paneA.getChildren().add(mineleft);
        minelefttext = new Label("10");
        paneA.getChildren().add(minelefttext);

        timespent = new Label("Timer:");
        paneA.getChildren().add(timespent);

        timespenttext = new Label();
        timespenttext.textProperty().bind(timeSeconds.asString());
        paneA.getChildren().add(timespenttext);

        //paneB
        VBox paneB = new VBox();
        paneB.setPadding(new Insets(10,20,10,10));
        root.getChildren().add(paneB);

        //add photo to paneB

        String path = "resources/smile.png"; // if in windows fix path
        Image image = new Image(new FileInputStream(path));

        //Setting the image view
        imageView = new ImageView(image);
        //fit the image view width to this number of pixels
        imageView.setFitWidth(60);
        //Preserve width & height ratio of the image in the image view
        imageView.setPreserveRatio(true);

        paneB.getChildren().add(imageView);


        //press smilingface to start the timer
        imageView.setOnMouseClicked(e-> {
            if (timeline != null) {
                timeline.stop();
            }
            timeSeconds.set(STARTTIME);
            timeline = new Timeline();
            timeline.getKeyFrames().add(
                    new KeyFrame(Duration.seconds(101),
                            new KeyValue(timeSeconds, 0)));
            timeline.playFromStart();
        });



        //pane C
        VBox paneC = new VBox();
        paneC.setPadding(new Insets(10,10,10,10));
        root.getChildren().add(paneC);

        dropping = new Label("Dropping to see results:\n  ");
        paneC.getChildren().add(dropping);

        //
        HBox panew = new HBox(createContent());
        panew.setPadding(new Insets(10,10,10,10));
        root.getChildren().add(panew);

        //Grid pane
        GridPane groot = new GridPane();
        groot.setVgap(1);
        groot.setHgap(1);
        root.getChildren().add(groot);
/*
        int i = 10;
        int j = 1;

        for (i = 10; i < 22; ++i)
            for (j = 1; j < 11; ++j) {
                Button btn = new Button(  "   ");
                groot.add(btn, i, j); // not use getChildren() as we set position
            }
*/

        //final Text source = new Text(50,100,"    ?");





        target.setOnDragOver(new EventHandler <DragEvent>() {
            public void handle(DragEvent event) {

                if (event.getGestureSource() != target &&
                        event.getDragboard().hasString()) {
                    event.acceptTransferModes(TransferMode.COPY_OR_MOVE);
                }

                event.consume();
            }
        });




        //groot.add(source,14,4);
        paneC.getChildren().add(target);

        buttonClose = new Button("Close");
        buttonClose.setPrefWidth(330);
        groot.add(buttonClose,10,17,21,17);
        buttonClose.setOnAction(buttonCloseListener);

        tutorial = new Text("Comments:\n1. Press Enter in the textfield to open a new window\n" +
                "2. Click on the smiling face to start the timer\n" +
                "3. Click any tile to open\n" +
                "4. Right click any tile to mark mine as a red tile\n" +
                "5. Right click any red tile to mark as a green tile\n" +
                "6. Dragging the green tile to the Dragging Area to see results\n" +
                "7. Click on Close to close the window\n" +
                "8. If opening a mine, it would print out 'Game Over'");
        groot.add(tutorial,10,50,20,50);
    }
}


// The script takes a reference from the following places
// 1. https://github.com/AlmasB/FXTutorials/blob/master/src/com/almasb/minesweeper/MinesweeperApp.java
// 2. https://docs.oracle.com/javafx/2/drag_drop/HelloDragAndDrop.java.html