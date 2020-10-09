from abc import abstractmethod, ABC

class MDP(ABC):
    """
    This class describes the interface for Markov Descision Process (MDP).
    Use as base class when to implementing specific processes.

    The interface is intended to allow for general probability and reward 
    methods, dependent on start state, action and end state. Simpler processes,
    dependent on e.g. only start state and action, or Markov Chains, can be
    implemented by letting the inheriting method accept the parameter, but ignore
    its value.

    The decorator @abstractmethod means that an error is raised if the
    corresponding method is not implemented when the child is instansiated.

    """

    @abstractmethod
    def P(self,s1,a,s2):
        """
        Probability of transitioning from state s1 to `s2` using action `a`.
        
       Parameters
        ----------
        s1 : 
           Start state
        a : 
           Action.
        s2 : 
           End state.
 
        Returns
        -------
        float in [0,1]
           Probability of transition.
        """
        pass


    @abstractmethod
    def R(self, s1, a, s2):
        """
        Reward associated with transitioning from state `s1` to `s2` using action `a`.

        Parameters
        ----------
        s1 : 
           Start state
        a : 
           Action.
        s2 : 
           End state.
        
        Returns
        -------
        float
           Reward of transition.
        """
        pass

    @abstractmethod
    def applicable_actions(self, s):
        """
        Get avaliable actions in state `s`.

        Parameters
        ----------
        s :
          State

        Returns
        -------
        set of actions
           Applicable choices as a list of actions.
        """
        pass

    @abstractmethod
    def successor_states(self,s,a):
        """
        Get list of sucessor states when choosing action `a` in state `s`.
        
        Parameters
        ----------
        s : state

        Returns
        -------
        set of states
        """
        pass

    @abstractmethod
    def states(self):
        """
        Get list of all possible states of process.
        
        Returns
        -------
        set of states
        """
        pass
