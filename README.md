# Identifying Files and Workflows Contributing to Technical Debt in GitHub Repositories Using Data Mining and Natural Language Processing Techniques

## Features

* **Fetching data from GitHub Actions Workflows**  
  Efficiently fetch data from GitHub Actions workflows for further analysis.

* **Data Cleaning**  
  Clean and preprocess the fetched data to ensure consistency and accuracy for downstream tasks.

* **Automatic Text Classification with NLP**  
  Leverage a pre-trained NLP model to automatically classify text,as TD and Not_TD instances

* **Technical Debt (TD) Visualization**  
  To visualize technical debt, we have generated insightful plots using popular Python libraries such as Matplotlib, Pandas, and Seaborn. These visualizations help to better understand the distribution and impact of technical debt across different aspects of the project.


## Installation

#### Prerequisites

Ensure that you have the following installed:

* [Python 3.8+](https://www.python.org/downloads/)

* [pip](https://pip.pypa.io/en/stable/)

#### Clone the repository

First, clone the project to your local machine:

```bash
git clone https://github.com/Aqila-Farahmand/MasterThesis
cd your-repository
```
### Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate    # For Linux/macOS
venv\Scripts\activate       # For Windows
```

### Install the dependencies
Use pip to install all the required packages from requirements.txt:

```bash
pip install -r requirements.txt
```
## Usage

### Running the Project

After installing the dependencies, you can run the project with:

* **Fetching Data**  
 To fetch the required data, run the following command: 

```bash
python -m data_fetching.__main__
```
   
* **Data Cleaning**
For data cleaning, you can use Google Colab or Jupyter Notebook. Import the file from ```data_cleaning/clean_data.ipynb``` and run the code there.


* **Text Classification** 
The text classification process uses an NLP model trained on a large dataset from GitHub issues. Due to GitHub's large file size limitations, only the inference code is provided in this repository.

* **Technical Debt (TD) Visualization**  
  You can generate simple plots to visualize your data using the script located at `data_visualization/workflow_analysis.py`. Simply run the file to create visualizations based on your dataset.


### Configuration

To fetch data, you'll need to configure authentication for making GitHub API requests.

1. Generate a [Personal Access Token (GITHUB_TOKEN)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) for authenticated API requests.

2. Set the `GITHUB_TOKEN` as an environment variable:

   ```bash
   env:
     GITHUB_TOKEN: ${{your_github_token}}


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

### Steps to contribute:

* Fork the repository
* Create a new branch (git checkout -b feature-branch)
* Commit your changes (git commit -m 'Add new feature')
* Push to the branch (git push origin feature-branch)
* Create a new pull request


## License

[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
