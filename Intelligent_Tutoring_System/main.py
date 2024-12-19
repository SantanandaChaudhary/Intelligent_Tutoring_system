import tkinter as tk
from tkinter import ttk, messagebox
from rdflib import Graph


class ShapeCalculator:
    def __init__(self, root, owl_file):
        self.root = root
        self.root.title("Shape Area and Perimeter Calculator")
        self.root.geometry("700x700")
        self.root.configure(bg="#f0f8ff")

        # Load OWL file
        self.owl_file = "main.owl"
        self.graph = Graph()
        self.graph.parse(self.owl_file, format="xml")
        self.shapes = self.get_shapes_from_ontology()

        self.last_formula = ""  # Store the last formula for the Hint button

        # Adding a modern style
        self.style = ttk.Style()
        self.style.configure("TRadiobutton", font=("Arial", 12), background="#f0f8ff", foreground="#333")
        self.style.configure("TButton", font=("Arial", 12), padding=10)
        self.style.map("TButton", background=[('active', '#cce7ff')])

        # Header
        header = tk.Frame(self.root, bg="#4da8da", height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="Shape Calculator", font=("Arial", 20, "bold"), bg="#4da8da", fg="white").pack(pady=10)

        # Shape selection
        tk.Label(root, text="Select a Shape:", font=("Arial", 14), bg="#f0f8ff").pack(pady=5)
        self.shape_var = tk.StringVar(value="Square")
        shape_frame = tk.Frame(root, bg="#f0f8ff")
        shape_frame.pack(pady=10)

        for shape in self.shapes:
            if shape != "Shape":  # Remove "Shape" button
                ttk.Radiobutton(
                    shape_frame,
                    text=shape,
                    variable=self.shape_var,
                    value=shape,
                    style="TRadiobutton",
                    command=self.update_inputs,
                ).pack(side=tk.LEFT, padx=15, pady=10)

        # Input fields
        self.inputs_frame = tk.Frame(root, bg="#f0f8ff")
        self.inputs_frame.pack(pady=20)
        self.update_inputs()

        # Buttons
        button_frame = tk.Frame(root, bg="#f0f8ff")
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Calculate Area", command=self.calculate_area, style="TButton").pack(side=tk.LEFT, padx=15)
        ttk.Button(button_frame, text="Calculate Perimeter", command=self.calculate_perimeter, style="TButton").pack(side=tk.LEFT, padx=15)
        ttk.Button(button_frame, text="Hint", command=self.show_hint, style="TButton").pack(side=tk.LEFT, padx=15)

        # Clear Button
        ttk.Button(root, text="Clear", command=self.clear, style="TButton").pack(pady=10)

        # Output
        self.output_label = tk.Label(root, text="", font=("Arial", 14), bg="#f0f8ff", fg="#333", justify="center", wraplength=600)
        self.output_label.pack(pady=10)

    def get_shapes_from_ontology(self):
        """Query the ontology for available shapes."""
        shapes_query = """
        SELECT DISTINCT ?shape WHERE {
            ?shape a <http://www.w3.org/2002/07/owl#Class> .
        }
        """
        result = self.graph.query(shapes_query)
        return [str(row[0].split("#")[-1]) for row in result]

    def update_inputs(self):
        """Update input fields dynamically based on selected shape."""
        for widget in self.inputs_frame.winfo_children():
            widget.destroy()

        shape = self.shape_var.get()
        if shape == "Triangle":
            tk.Label(self.inputs_frame, text="Base:", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=0, padx=5, pady=5)
            self.base_entry = ttk.Entry(self.inputs_frame, font=("Arial", 12))
            self.base_entry.grid(row=0, column=1, padx=5, pady=5)

            tk.Label(self.inputs_frame, text="Height:", font=("Arial", 12), bg="#f0f8ff").grid(row=1, column=0, padx=5, pady=5)
            self.height_entry = ttk.Entry(self.inputs_frame, font=("Arial", 12))
            self.height_entry.grid(row=1, column=1, padx=5, pady=5)

            tk.Label(self.inputs_frame, text="Side 1:", font=("Arial", 12), bg="#f0f8ff").grid(row=2, column=0, padx=5, pady=5)
            self.side1_entry = ttk.Entry(self.inputs_frame, font=("Arial", 12))
            self.side1_entry.grid(row=2, column=1, padx=5, pady=5)

            tk.Label(self.inputs_frame, text="Side 2:", font=("Arial", 12), bg="#f0f8ff").grid(row=3, column=0, padx=5, pady=5)
            self.side2_entry = ttk.Entry(self.inputs_frame, font=("Arial", 12))
            self.side2_entry.grid(row=3, column=1, padx=5, pady=5)

            tk.Label(self.inputs_frame, text="Side 3:", font=("Arial", 12), bg="#f0f8ff").grid(row=4, column=0, padx=5, pady=5)
            self.side3_entry = ttk.Entry(self.inputs_frame, font=("Arial", 12))
            self.side3_entry.grid(row=4, column=1, padx=5, pady=5)

        elif shape == "Square":
            tk.Label(self.inputs_frame, text="Side Length:", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=0, padx=5, pady=5)
            self.side_entry = ttk.Entry(self.inputs_frame, font=("Arial", 12))
            self.side_entry.grid(row=0, column=1, padx=5, pady=5)

        elif shape == "Rectangle":
            tk.Label(self.inputs_frame, text="Length:", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=0, padx=5, pady=5)
            self.length_entry = ttk.Entry(self.inputs_frame, font=("Arial", 12))
            self.length_entry.grid(row=0, column=1, padx=5, pady=5)

            tk.Label(self.inputs_frame, text="Width:", font=("Arial", 12), bg="#f0f8ff").grid(row=1, column=0, padx=5, pady=5)
            self.width_entry = ttk.Entry(self.inputs_frame, font=("Arial", 12))
            self.width_entry.grid(row=1, column=1, padx=5, pady=5)

        elif shape == "Sphere":
            tk.Label(self.inputs_frame, text="Radius:", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=0, padx=5, pady=5)
            self.radius_entry = ttk.Entry(self.inputs_frame, font=("Arial", 12))
            self.radius_entry.grid(row=0, column=1, padx=5, pady=5)

    def calculate_area(self):
        shape = self.shape_var.get()
        try:
            if shape == "Triangle":
                base = self.base_entry.get()
                height = self.height_entry.get()
                if not base or not height:
                    raise ValueError("Please input the Base and Height of your Triangle.")
                area = 0.5 * float(base) * float(height)
                self.last_formula = "Area = 0.5 × Base × Height"
            elif shape == "Square":
                side = self.side_entry.get()
                if not side:
                    raise ValueError("Please input the Side of your Square.")
                area = float(side) ** 2
                self.last_formula = "Area = Side × Side"
            elif shape == "Rectangle":
                length = self.length_entry.get()
                width = self.width_entry.get()
                if not length or not width:
                    raise ValueError("Please input the Length and Width of your Rectangle.")
                area = float(length) * float(width)
                self.last_formula = "Area = Length × Width"
            elif shape == "Sphere":
                radius = self.radius_entry.get()
                if not radius:
                    raise ValueError("Please input the Radius of your Sphere.")
                area = 4 * 3.14159 * (float(radius) ** 2)
                self.last_formula = "Area = 4 × π × Radius²"
            else:
                area = 0
                self.last_formula = ""
            self.output_label.config(text=f"Area of {shape}: {area:.2f}")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def calculate_perimeter(self):
        shape = self.shape_var.get()
        try:
            if shape == "Triangle":
                side1 = self.side1_entry.get()
                side2 = self.side2_entry.get()
                side3 = self.side3_entry.get()
                if not side1 or not side2 or not side3:
                    raise ValueError("Please input all three sides of your Triangle.")
                perimeter = float(side1) + float(side2) + float(side3)
                self.last_formula = "Perimeter = Side1 + Side2 + Side3"
            elif shape == "Square":
                side = self.side_entry.get()
                if not side:
                    raise ValueError("Please input the Side of your Square.")
                perimeter = 4 * float(side)
                self.last_formula = "Perimeter = 4 × Side"
            elif shape == "Rectangle":
                length = self.length_entry.get()
                width = self.width_entry.get()
                if not length or not width:
                    raise ValueError("Please input the Length and Width of your Rectangle.")
                perimeter = 2 * (float(length) + float(width))
                self.last_formula = "Perimeter = 2 × (Length + Width)"
            else:
                perimeter = "Not applicable"
                self.last_formula = ""
            self.output_label.config(text=f"Perimeter of {shape}: {perimeter}")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def show_hint(self):
        if self.last_formula:
            messagebox.showinfo("Hint", f"Formula: {self.last_formula}")
        else:
            messagebox.showinfo("Hint", "No formula available. Perform a calculation first.")

    def clear(self):
        for widget in self.inputs_frame.winfo_children():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
        self.output_label.config(text="")
        self.last_formula = ""


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    owl_file_path = "/mnt/data/main.owl"
    app = ShapeCalculator(root, owl_file=owl_file_path)
    root.mainloop()
