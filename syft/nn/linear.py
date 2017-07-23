from syft import he
import numpy as np

class LinearClassifier():
    """This class is a basic linear classifier with functionality to encrypt/decrypt
    weights according to any of the homomorphic encryption schemes in syft.he. It also
    contains the logic to make predictions when in an encrypted state.

    TODO: create a generic interface for ML models that this class implements.

    TODO: minibatching in the "learn" API. The greater the batch size, the more
    iterations should be doable before the homomorphic encryption noise grows too
    much to be decrypted.
    """


    def __init__(self,n_inputs=4,n_labels=2,desc=""):

        self.desc = desc

        self.n_inputs = n_inputs
        self.n_labels = n_labels

        self.weights = list()
        for i in range(n_inputs):
            self.weights.append(np.zeros(n_labels).astype('float64'))

        self.pubkey = None
        self.encrypted = False

    def encrypt(self,pubkey):
        """iterates through each weight and encrypts it

        TODO: check that weights are actually decrypted

        """

        self.encrypted = True
        self.pubkey = pubkey
        for i,w in enumerate(self.weights):
            self.weights[i] = self.pubkey.encrypt(w)
        return self

    def decrypt(self,seckey):
        """iterates through each weight and decrypts it

        TODO: check that weights are actually encrypted

        """
        self.encrypted = False
        for i,w in enumerate(self.weights):
            self.weights[i] = seckey.decrypt(w)
        return self

    def forward(self,input):

        """Makes a prediction based on input. If the network is encrypted, the
        prediction is also encrypted and vise versa."""

        pred = self.weights[0] * input[0]
        for j,each_inp in enumerate(input[1:]):
            if(each_inp == 1):
                pred = pred + self.weights[j+1]
            elif(each_inp != 0):
                pred = pred + (self.weights[j+1] * input[j+1])

        return pred

    def generate_gradient(self,input,target):
        target = np.array(target).astype('float64')
        pred = self.forward(input)

        target_v = target

        if(self.pubkey is not None and self.encrypted == True):
            target_v = self.pubkey.encrypt(target_v)

        output_grad = (pred - target_v)

        weight_grad = np.zeros_like(self.weights)

        if(self.encrypted):
            weight_grad = self.pubkey.encrypt(weight_grad)

        for i in range(len(input)):
            if(input[i] != 1 and input[i] != 0):
                weight_grad[i] += (output_grad * input[i])
            elif(input[i] == 1):
                weight_grad[i] += output_grad
            else:
                "doesn't matter... input == 0"

        return weight_grad


    def learn(self,input,target,alpha=0.5):
        """Updates weights based on input and target prediction. Note, updating
        weights increases the noise in the encrypted weights and will eventually
        require the weights to be re-encrypted.

        TODO: minibatching
        TODO: instead of storing weights, store aggregated weight updates (and
        optionally use them in "forward").

        """

        weight_update = self.generate_gradient(input,target)
        self.weights -= weight_update * alpha

        return weight_update

    def evaluate(self,inputs,targets):
        """accepts a list of inputs and a list of targets - returns the mean squared
        error scaled by a fixed amount and converted to an integer."""

        scale = 1000

        if(self.encrypted == True):
            return "not yet supported... but will in the future"
        else:

            loss = 0
            for i,row in enumerate(inputs):
                pred = self.forward(row)
                true = targets[i]
                loss += (pred - true)**2
            return int((loss[0]*scale)/float(len(inputs)))


    def __str__(self):
        return "Linear Model ("+str(self.n_inputs)+","+str(self.n_labels)+"): " + str(self.desc)

    def __repr__(self):
        return self.__str__()
