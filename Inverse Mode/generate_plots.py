import matplotlib.pyplot as plt
import numpy as np
#from PIL import Image
import io

def plot_1D(data_list,dynamics, model, fig_name):

    plot_1D_cell(data_list, dynamics, model, fig_name[1:])
    plot_1D_array(data_list, dynamics, model, fig_name[1:])
    plot_1D_grid(dynamics, model, fig_name[1:])
    return 0

def plot_1D_cell(data_list, dynamics, model, fig_name):

    ## Unpack data
    observe_x, observe_train, v_train, v = data_list[0], data_list[1], data_list[2], data_list[3]

    ## Pick a cell to show
    cell = dynamics.max_x*0.75
    lnw = 3.0 # line width
    szm = 50 # marker size
    ftsz = 20 # font size

    ## Get data for cell
    idx = [i for i,ix in enumerate(observe_x) if observe_x[i][0]==cell]
    observe_geomtime = observe_x[idx]
    v_GT = v[idx]
    v_predict = model.predict(observe_geomtime)[:,0:1]
    t_axis = observe_geomtime[:,1]

    ## Get data for points used in training process
    idx_train = [i for i,ix in enumerate(observe_train) if observe_train[i][0]==cell]
    v_trained_points = v_train[idx_train]
    t_markers = (observe_train[idx_train])[:,1]

    ## create figure
    plt.figure()
    plt.rc('font', size= ftsz) #controls default text
    fig, ax = plt.subplots()
    GT, = ax.plot(t_axis, v_GT, c='b', label='GT',linewidth=lnw, linestyle = 'dashed', zorder=0)
    Predicted, = ax.plot(t_axis, v_predict, c='r', label='Predicted',linewidth=lnw, zorder=5)
    #plt.scatter(t_axis, v_predict, marker='x', c='r',s=szm, label='Predicted2')
    # If there are any trained data points for the current cell
    if len(t_markers):
        Observed = ax.scatter(t_markers, v_trained_points, marker='x', c='black',s=szm, label='Observed', zorder=10)
    #plt.legend(ncol = 2, loc = 'lower center', fontsize = ftsz)
    #lines = ax.get_lines()
    #first_legend = plt.legend([lines[i] for i in [0,1]], ["GT", "Predicted"], loc='lower center')
    #ax.add_artist(first_legend)
    #second_legend = plt.legend(lines[2], ["Observed"], loc=2)
    #ax.add_artist(second_legend)
    #plt.legend(handles=[Observed], borderpad=0.2)
    plt.legend(loc='top right', borderpad=0.2)
    plt.xlabel('t (TU)', fontsize = ftsz)
    plt.ylabel('u (AU)', fontsize = ftsz)
    plt.ylim((-0.2,1.2))

    ## save figure
    # png1 = io.BytesIO()
    plt.savefig(fig_name + "_cell_plot_1D.png", format="png", dpi=500, pad_inches = .1, bbox_inches = 'tight')
    # plt.savefig(png1, format="eps", dpi=500, pad_inches = .1, bbox_inches = 'tight')
    plt.savefig(fig_name + "_cell_plot_1D.svg", format="svg", dpi=500, pad_inches = .1, bbox_inches = 'tight')
#    png2 = Image.open(png1)
#    png2.save(fig_name + "_cell_plot_1D.tiff")
    # png1.close()
    return 0

def plot_1D_array(data_list, dynamics, model, fig_name):
    lnw = 3.0 # line width
    szm = 26 # marker size
    ftsz = 20 # font size

    ## Unpack data
    observe_x, observe_train, v_train, v = data_list[0], data_list[1], data_list[2], data_list[3]

    ## Pick a point in time to show
    obs_t = dynamics.max_t/2

    ## Get all array data for chosen time
    idx = [i for i,ix in enumerate(observe_x) if observe_x[i][1]==obs_t]
    observe_geomtime = observe_x[idx]
    v_GT = v[idx]
    v_predict = model.predict(observe_geomtime)[:,0:1]
    x_ax = observe_geomtime[:,0]

    ## Get data for points used in training process
    idx_train = [i for i,ix in enumerate(observe_train) if observe_train[i][1]==obs_t]
    v_trained_points = v_train[idx_train]
    x_markers = (observe_train[idx_train])[:,0]

    ## create figure
    plt.figure()
    plt.rc('font', size= ftsz) #controls default text size
    plt.plot(x_ax, v_GT, c='b', label='GT',linewidth=lnw, linestyle = 'dashed')
    plt.plot(x_ax, v_predict, c='r', label='Predicted',linewidth=lnw)
    #plt.scatter(x_ax, v_predict, marker='x', c='r',s=szm, label='Predicted2')
    # If there are any trained data points for the current time step
    if len(x_markers):
        plt.scatter(x_markers, v_trained_points, marker='x', c='black',s=szm, label='Observed')
    plt.legend(fontsize = ftsz, loc = 'lower center')
    plt.xlabel('x (mm)', fontsize = ftsz)
    plt.ylabel('u (AU)', fontsize = ftsz)
    plt.ylim((-0.2,1.2))

    ## save figure
    # png1 = io.BytesIO()
    plt.savefig(fig_name + "_array_plot_1D.png", format="png", dpi=500, pad_inches = .1, bbox_inches = 'tight')
    # plt.savefig(png1, format="eps", dpi=500, pad_inches = .1, bbox_inches = 'tight')
    plt.savefig(fig_name + "_array_plot_1D.svg", format="svg", dpi=500, pad_inches = .1, bbox_inches = 'tight')
#    png2 = Image.open(png1)
#    png2.save(fig_name + "_array_plot_1D.tiff")
    # png1.close()
    return 0

def plot_1D_grid(dynamics, model, fig_name):
    lnw = 3.0 # line width
    szm = 26 # marker size
    ftsz = 20 # font size
    grid_size = 200

    ## Get data
    x = np.linspace(dynamics.min_x,dynamics.max_x, grid_size)
    t = np.linspace(dynamics.min_t,dynamics.max_t,grid_size)
    X, T = np.meshgrid(x,t)
    X_data = X.reshape(-1,1)
    T_data = T.reshape(-1,1)
    data = np.hstack((X_data, T_data))
    v_pred = model.predict(data)[:,0:1]
    Z = np.zeros((grid_size,grid_size))
    for i in range(grid_size):
        Z[i,:] = (v_pred[(i*grid_size):((i+1)*grid_size)]).reshape(-1)

    ## create figure
    plt.figure()
    plt.rc('font', size= ftsz) #controls default text size
    contour = plt.contourf(T,X,Z, levels = np.arange(-0.15,1.06,0.15) , cmap=plt.cm.bone)
    plt.xlabel('t (TU)', fontsize = ftsz)
    plt.ylabel('x (mm)', fontsize = ftsz)
    cbar = plt.colorbar(contour)
    cbar.ax.set_ylabel('U (AU)', fontsize = ftsz)

    ## save figure
    # png1 = io.BytesIO()
    plt.savefig(fig_name + "_grid_plot_1D.png", format="png", dpi=500, pad_inches = .1, bbox_inches = 'tight')
    # plt.savefig(png1, format="eps", dpi=500, pad_inches = .1, bbox_inches = 'tight')
    plt.savefig(fig_name + "_grid_plot_1D.svg", format="svg", dpi=500, pad_inches = .1, bbox_inches = 'tight')
#    png2 = Image.open(png1)
#    png2.save(fig_name + "_grid_plot_1D.tiff")
    # png1.close()
    return 0
