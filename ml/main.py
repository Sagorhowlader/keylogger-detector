from train_model import TrainModel

if __name__ == "__main__":

    trainer = TrainModel(csv_path="data/prepared_dataset.csv", output_dir="models/trained_model")
    trainer.train_and_save_all()