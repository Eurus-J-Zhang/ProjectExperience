package view;

import javafx.geometry.Insets;
import javafx.scene.control.Label;
import javafx.scene.layout.GridPane;

public class WelcomeView extends GridPane {
    public WelcomeView() {

        this.setPadding(new Insets(10, 10, 10, 10));
        this.setMinSize(100, 100);
        this.setVgap(5);
        this.setHgap(5);

        Label l = new Label("Hello, welcome to the game!");
        this.add(l, 0, 4, 4, 1); // adding a control across multiple cells
    }
}
