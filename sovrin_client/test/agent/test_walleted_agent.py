from plenum.common.log import getlogger
from plenum.common.types import f
from plenum.test.testable import Spyable

from sovrin_client.agent.agent import WalletedAgent, createAndRunAgent
from sovrin_client.client.client import Client
from sovrin_common.exceptions import LinkNotFound
from sovrin_common.txn import NONCE
from sovrin_client.test.agent.helper import getAgentCmdLineParams

logger = getlogger()


@Spyable(
    methods=[WalletedAgent._handlePing, WalletedAgent._handlePong])
class TestWalletedAgent(WalletedAgent):
    def getLinkForMsg(self, msg):
        nonce = msg.get(NONCE)
        identifier = msg.get(f.IDENTIFIER.nm)
        link = None
        for _, li in self.wallet._links.items():
            if li.invitationNonce == nonce and li.remoteIdentifier == identifier:
                link = li
                break
        if link:
            return link
        else:
            raise LinkNotFound

    @staticmethod
    def getPassedArgs():
        return getAgentCmdLineParams()


    def createAndRunAgent(agentClass, name, wallet=None, basedirpath=None,
                      port=None, looper=None, clientClass=Client, bootstrap=True):
        try:
            return createAndRunAgent(agentClass=agentClass, name=name,
                                      wallet=wallet, basedirpath=basedirpath,
                                      port=port, looper=looper,
                                      clientClass=clientClass, bootstrap=bootstrap)
        except Exception as exc:
            logger.error(str(exc))