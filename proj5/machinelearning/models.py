import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(self.w, x)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        dot = nn.as_scalar(self.run(x))
        return 1 if dot >= 0 else -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        batch_size, done = 1, False
        while not done:
            done = True
            for x, y in dataset.iterate_once(batch_size):
                res = self.get_prediction(x)
                if res != nn.as_scalar(y):
                    self.w.update(nn.Constant(nn.as_scalar(y) * x.data), 1)
                    done = False

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.multiplier = 0.02
        self.m1 = nn.Parameter(1, 128)
        self.b1 = nn.Parameter(1, 128)
        self.m2 = nn.Parameter(128, 64)
        self.b2 = nn.Parameter(1, 64)
        self.m3 = nn.Parameter(64, 32)
        self.b3 = nn.Parameter(1, 32)
        self.m4 = nn.Parameter(32, 1)
        self.b4 = nn.Parameter(1, 1)
        self.hyp = [self.m1, self.b1, self.m2, self.b2, self.m3, self.b3, self.m4, self.b4]

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        layer1 = nn.ReLU(nn.AddBias(nn.Linear(x, self.m1), self.b1))
        layer2 = nn.ReLU(nn.AddBias(nn.Linear(layer1, self.m2), self.b2))
        layer3 = nn.ReLU(nn.AddBias(nn.Linear(layer2, self.m3), self.b3))
        output_layer = nn.AddBias(nn.Linear(layer3, self.m4), self.b4)
        return output_layer

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss nodes
        """
        "*** YOUR CODE HERE ***"
        return nn.SquareLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 1
        loss = float('inf')
        while loss >= 0.02:
            for x, y in dataset.iterate_once(batch_size):
                grads = nn.gradients(self.get_loss(x, y), self.hyp)
                loss = nn.as_scalar(self.get_loss(x, y))
                for i in range(len(self.hyp)):
                    self.hyp[i].update(grads[i], -self.multiplier)

class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.multiplier = 0.05
        self.m1 = nn.Parameter(784, 256)
        self.b1 = nn.Parameter(1, 256)
        self.m2 = nn.Parameter(256, 128)
        self.b2 = nn.Parameter(1, 128)
        self.m3 = nn.Parameter(128, 64)
        self.b3 = nn.Parameter(1, 64)
        self.m4 = nn.Parameter(64, 10)
        self.b4 = nn.Parameter(1, 10)
        self.hyp = [self.m1, self.b1, self.m2, self.b2, self.m3, self.b3, self.m4, self.b4]

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        layer1 = nn.ReLU(nn.AddBias(nn.Linear(x, self.m1), self.b1))
        layer2 = nn.ReLU(nn.AddBias(nn.Linear(layer1, self.m2), self.b2))
        layer3 = nn.ReLU(nn.AddBias(nn.Linear(layer2, self.m3), self.b3))
        output_layer = nn.AddBias(nn.Linear(layer3, self.m4), self.b4)
        return output_layer

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 100
        loss = float('inf')
        acc = 0
        while acc < .98:
            for x, y in dataset.iterate_once(batch_size):
                grads = nn.gradients(self.get_loss(x, y), self.hyp)
                loss = nn.as_scalar(self.get_loss(x, y))
                for i in range(len(self.hyp)):
                    self.hyp[i].update(grads[i], -self.multiplier)
            acc = dataset.get_validation_accuracy()

class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.multiplier = 0.1
        self.m1 = nn.Parameter(self.num_chars, 256)
        self.b1 = nn.Parameter(1, 256)
        self.m2 = nn.Parameter(256, 256)
        self.x2 = nn.Parameter(self.num_chars, 256)
        self.b2 = nn.Parameter(1, 256)
        self.m3 = nn.Parameter(256, len(self.languages))
        self.b3 = nn.Parameter(1, len(self.languages))
        self.hyp = [self.m1, self.b1, self.m2, self.b2, self.m3, self.b3]

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        layer = nn.ReLU(nn.AddBias(nn.Linear(xs[0], self.m1), self.b1))
        for x in xs[1:]:
            layer = nn.ReLU(nn.AddBias(nn.Add(nn.Linear(x, self.x2), nn.Linear(layer, self.m2)), self.b2))
        output_layer = nn.AddBias(nn.Linear(layer, self.m3), self.b3)
        return output_layer

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(xs), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 100
        loss = float('inf')
        acc = 0
        while acc < .85:
            for x, y in dataset.iterate_once(batch_size):
                grads = nn.gradients(self.get_loss(x, y), self.hyp)
                loss = nn.as_scalar(self.get_loss(x, y))
                for i in range(len(self.hyp)):
                    self.hyp[i].update(grads[i], -self.multiplier)
            acc = dataset.get_validation_accuracy()
