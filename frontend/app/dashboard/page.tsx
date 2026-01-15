'use client';

import React from 'react';
import ProtectedRoute from '../components/auth/ProtectedRoute';
import MainLayout from '../components/layout/MainLayout';
import TaskList from '../components/tasks/TaskList';
import TaskForm from '../components/tasks/TaskForm';
import { useTasks } from '../hooks/useTasks';
import { TaskCreateRequest } from '../lib/types';

const DashboardPage: React.FC = () => {
  const {
    tasks,
    loading,
    error,
    createTask,
    updateTask,
    toggleTaskCompletion,
    deleteTask,
  } = useTasks();

  const handleTaskSubmit = async (data: TaskCreateRequest) => {
    try {
      await createTask(data);
    } catch (err) {
      console.error('Failed to create task:', err);
    }
  };

  const handleTaskUpdate = async (taskId: string, updatedTask: Partial<TaskCreateRequest>) => {
    try {
      await updateTask(taskId, updatedTask);
    } catch (err) {
      console.error('Failed to update task:', err);
    }
  };

  const handleTaskDelete = async (taskId: string) => {
    try {
      await deleteTask(taskId);
    } catch (err) {
      console.error('Failed to delete task:', err);
    }
  };

  return (
    <ProtectedRoute>
      <MainLayout title="Dashboard">
        <div className="max-w-3xl mx-auto">
          {error && (
            <div className="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
              <strong className="font-bold">Error: </strong>
              <span className="block sm:inline">{error}</span>
            </div>
          )}

          <div className="bg-white shadow rounded-lg p-6 mb-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Create New Task</h2>
            <TaskForm onSubmit={handleTaskSubmit} submitText="Create Task" />
          </div>

          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Your Tasks</h2>
            <TaskList
              tasks={tasks}
              onTaskUpdate={handleTaskUpdate}
              onTaskDelete={handleTaskDelete}
            />
          </div>
        </div>
      </MainLayout>
    </ProtectedRoute>
  );
};

export default DashboardPage;