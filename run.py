from caltech_dataset import Caltech

if __name__ == '__main__':
    train_dataset = Caltech(root='./101_ObjectCategories', split='train', transform=None)
    data = train_dataset.get_data()