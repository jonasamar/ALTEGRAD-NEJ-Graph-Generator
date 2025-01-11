# Graph Generation and Data Augmentation

This repository contains scripts to generate synthetic graphs and prompts, integrate them into a training dataset, and retrain a graph-based model for enhanced performance.

## **Step-by-Step Guide for Data Augmentation**

### **1. Generate New Prompts**
Use the `prompt_generator.py` script to create synthetic prompts following the distribution of properties observed in the training data.

```bash
python code/data_augmentation/prompt_generator.py --output new_prompts.txt --num-prompts 1000
```

This script will:
- Sample graph characteristics (nodes, edges, clustering coefficient, etc.) from the original distribution.
- Save each new prompt in a format compatible with the test set.
- Write the prompts to a specified output file.

### **2. Generate Graphs from Prompts**
Run the `main.py` script in inference mode to generate graphs conditioned on the synthetic prompts.

Make sure your trained model is available for inference. This will create a CSV file containing the graph structures for each prompt.

### **3. Convert Generated Outputs to Training Data**
Use `new_dataset.py` to convert the CSV into individual graph and prompt files.

```bash
python code/data_augmentation/new_dataset.py --input outputs.csv --output-dir augmented_dataset
```

This script will:
- Extract graph structures and prompts from the CSV.
- Save each graph in `.edgelist` format.
- Create a description file with recalculated properties for each graph.

### **4. Integrate Augmented Data into the Training Set**
Move the `augmented_dataset` files into your training set directory and retrain the model using `main.py`.
