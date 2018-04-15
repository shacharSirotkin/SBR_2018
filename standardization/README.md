# Standardization
The resources for the plan recognition standardization project

## Domains
These domains are based on the domains from the following publications:

- 1-5-2-3-4-full: *Kabanza et al. Controlling the hypothesis space in probabilistic plan recognition. IJCAI. 2013.*
A simulated domain based on and/or trees. The values in the name represent the characretirsics of the domain - 1 plan execution, 5 possible goals, or-branching of 2, and-branching of 3, depth of 4, fully ordered. This domain has no parameters.

## Algorithms
The following algorithms support the use of this XML format:

- SBR: *Dorit Avrahami-Zilberbrand and Gal A. Kaminka. Fast and Complete Symbolic Plan Recognition. In Proceedings of the International Joint Conference on Artificial Intelligence (IJCAI-05), pp. 653–658, 2005.*
A complete algorithm for plan recognition. Does not handle exogenous actions and partial ordering. It contains tree parts in a pipeline - FDT,CSQ and HSQ. Their code is available online, soon will be able to handle parameters.

- PHATT *Geib and Goldman. A probabilistic plan recognition algorithm based on plan tree grammars. Artificial Intelligence173.11. 2009. 1101-1132.* A complete algorithm for plan recognition. Handles partial ordering and interleaving plans.

- CRADLE *Reuth Mirsky, Ya'akov  Gal, Stuart Shieber. CRADLE: An Online Plan Recognition Algorithm for Exploratory Domains. ACM Transactions on Intelligent Systems and Technology*
CRADLE is a heuristic algorithm, based on PHATT. Can handle parameter-binding, exogenous actions, partial ordering and filters. When turning these modules off, you basically get PHATT.


