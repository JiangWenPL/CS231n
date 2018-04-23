import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_classes = W.shape[1]
  num_train = X.shape[0]
  for i in xrange(num_train):
    scores = X[i].dot(W)
    scores -= np.max(scores)
    sum_exp = np.sum(np.exp(scores))
    loss += -scores[y[i]] + np.log(sum_exp)
    for j in xrange(num_classes):
      if j==y[i]:
        dW[:,j] += -X[i] + X[i] * np.exp(scores[j])/sum_exp
      else:
        dW[:,j] += X[i] * np.exp(scores[j])/sum_exp
  loss /= num_train
  dW /= num_train
  loss += reg * np.sum(W * W)
  dW += reg * 2 * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_classes = W.shape[1]
  num_train = X.shape[0]
  scores = X.dot(W)
#   print(np.max(scores, axis=1).shape)
  scores -= np.max(scores, axis=1).reshape(-1,1)
  sum_exp = np.sum(np.exp(scores), axis=1)
  loss += -np.sum(scores[range(num_train),y]) + np.sum(np.log(sum_exp))
#   print(dW[:,0].shape, X[0].shape)
  mask = np.zeros((num_train,num_classes))
  mask[np.arange(num_train),y] = 1
  dW -= X.T.dot(mask)
  dW += (X/sum_exp.reshape(-1,1)).T.dot(np.exp(scores))
  loss /= num_train
  dW /= num_train
  loss += reg * np.sum(W * W)
  dW += reg * 2 * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

       